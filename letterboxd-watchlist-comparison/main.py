import os
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from scraper import scrape_user_watchlist, build_session
from tmdb import TMDbClient
from gui import LetterboxdGUI
from utils import get_film_key

# --- Load config ---
with open("config.json") as f:
    config = json.load(f)

user_groups = config.get("user_groups", [])
user_map = config.get("user_map", {})
OUTPUT_DIR = config.get("output_dir", "letterboxd_watchlists")
COMBINED_FILENAME = config.get("combined_filename", "combined_watchlist.csv")
COMBINED_PATH = os.path.join(OUTPUT_DIR, COMBINED_FILENAME)
API_KEY = config.get("tmdb_api_key", "")
COUNTRY = config.get("country", "GB")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Helper functions ---
def merge_combined(user_films_map, existing_df=None):
    merged = {}

    if existing_df is not None:
        for _, row in existing_df.iterrows():
            key = (row['title'], str(row['year']).strip())
            merged[key] = {**row, "users": set(str(row.get("users","")).split(","))}

    for username, films in user_films_map.items():
        display_name = user_map.get(username, username)
        for film in films:
            key = get_film_key(film)
            if not key[0]:
                continue
            if key not in merged:
                merged[key] = {
                    "title": key[0],
                    "year": key[1],
                    "tmdb_id": "",
                    "overview": "",
                    "genres": "",
                    "runtime": pd.NA,
                    "providers": "",
                    "poster_url": "",
                    "users": set()
                }
            merged[key]["users"].add(display_name)

    rows = [{
        "title": d["title"],
        "year": d["year"],
        "tmdb_id": d.get("tmdb_id",""),
        "overview": d.get("overview",""),
        "genres": d.get("genres",""),
        "runtime": d.get("runtime", pd.NA),
        "providers": d.get("providers",""),
        "poster_url": d.get("poster_url",""),
        "users": ", ".join(sorted(d["users"]))
    } for d in merged.values()]

    df = pd.DataFrame(rows)
    df = df[["title","year","tmdb_id","overview","genres","runtime","providers","poster_url","users"]]
    df.to_csv(COMBINED_PATH, index=False)
    return df

def load_watchlists():
    all_watchlists = {}
    if not os.path.isfile(COMBINED_PATH):
        return all_watchlists
    df = pd.read_csv(COMBINED_PATH, dtype=str).fillna("")
    df['year'] = df['year'].str.strip().str.replace('.0','',regex=False)
    for _, row in df.iterrows():
        film = {k: row.get(k,"") for k in ["title","year","tmdb_id","overview","genres","runtime","providers","poster_url"]}
        for user in [u.strip() for u in row.get("users","").split(",") if u.strip()]:
            all_watchlists.setdefault(user, []).append(film)
    return all_watchlists

# --- Scraping & Merging ---
def scrape_all_users():
    all_results = {}
    session = build_session()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for group in user_groups:
            for username in group:
                futures.append(executor.submit(scrape_user_watchlist, username, session))
        for i, fut in enumerate(futures):
            username = [u for g in user_groups for u in g][i]
            all_results[username] = fut.result()
    session.close()
    return all_results

# --- TMDb Enrichment ---
def enrich_combined():
    if not os.path.isfile(COMBINED_PATH) or not API_KEY:
        return
    df = pd.read_csv(COMBINED_PATH, dtype=str).fillna("")
    for col in ["tmdb_id","overview","genres","providers","poster_url"]:
        df[col] = df.get(col,"").fillna("")
    df["runtime"] = pd.to_numeric(df.get("runtime", pd.NA), errors="coerce")
    to_enrich = df[df["tmdb_id"].isna() | (df["tmdb_id"]=="")]
    client = TMDbClient(API_KEY, COUNTRY)
    for i, row in to_enrich.iterrows():
        film = {"title": row["title"], "year": str(row.get("year","")).strip()}
        enriched = client.enrich_film(film)
        df.at[i,"tmdb_id"] = enriched.get("tmdb_id","")
        df.at[i,"overview"] = enriched.get("overview","")
        df.at[i,"genres"] = enriched.get("genres","")
        df.at[i,"runtime"] = enriched.get("runtime") or pd.NA
        df.at[i,"poster_url"] = enriched.get("poster_url","")
        df.at[i,"providers"] = enriched.get("providers","")
    df.to_csv(COMBINED_PATH, index=False)

# --- Main scraping workflow ---
def scrape_merge_enrich(callback=None):
    existing_df = pd.read_csv(COMBINED_PATH, dtype=str) if os.path.isfile(COMBINED_PATH) else None
    user_films = scrape_all_users()
    merge_combined(user_films, existing_df)
    enrich_combined()
    if callback:
        callback()

# --- Run GUI ---
if __name__ == "__main__":
    # Load existing watchlists
    all_watchlists = load_watchlists()

    # Launch GUI
    LetterboxdGUI(all_watchlists, scrape_merge_enrich)
