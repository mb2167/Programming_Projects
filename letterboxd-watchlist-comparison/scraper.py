import time, re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter, Retry
from utils import clean_year, get_film_key

REQUEST_DELAY = 0.4

def build_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    })
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=(429,500,502,503,504), allowed_methods=("GET",))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    return session

def parse_watchlist_page(soup):
    films = []
    for t in soup.select('div.react-component[data-component-class="LazyPoster"]'):
        title_raw = (t.get("data-item-name") or "").strip()
        link = t.get("data-item-link") or ""
        film_id = t.get("data-film-id") or ""
        title, year = "", ""
        m = re.match(r'^(.*?)\s*\((\d{4})\)\s*$', title_raw)
        if m:
            title, year = m.group(1).strip(), m.group(2).strip()
        elif "(" in title_raw and title_raw.endswith(")"):
            title = title_raw[:title_raw.rfind("(")].strip()
            year = title_raw[title_raw.rfind("(")+1:title_raw.rfind(")")].strip()
        else:
            title = title_raw
        films.append({"title": title, "year": clean_year(year), "link": link, "film_id": film_id})
    return films

def scrape_user_watchlist(username, session=None):
    if session is None:
        session = build_session()
    url = f"https://letterboxd.com/{username}/watchlist/"
    all_films, visited = [], set()
    try:
        while url and url not in visited:
            visited.add(url)
            r = session.get(url, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            all_films.extend(parse_watchlist_page(soup))
            next_a = soup.select_one("a.next")
            url = urljoin("https://letterboxd.com", next_a.get("href")) if next_a else None
            time.sleep(REQUEST_DELAY)
        # Deduplicate
        seen, deduped = set(), []
        for f in all_films:
            key = get_film_key(f)
            if key[0] and key not in seen:
                seen.add(key)
                deduped.append({"title": key[0], "year": key[1]})
        return deduped
    except Exception as e:
        print(f"Error scraping {username}: {e}")
        return []
