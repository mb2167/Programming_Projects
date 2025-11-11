import requests
import time
from utils import clean_year

TMDB_API_BASE = "https://api.themoviedb.org/3"
RATE_LIMIT_DELAY = 0.2

class TMDbClient:
    def __init__(self, api_key, country="GB"):
        self.api_key = api_key
        self.country = country

    def search_movie(self, title, year=None):
        try:
            r = requests.get(
                f"{TMDB_API_BASE}/search/movie",
                params={"api_key": self.api_key, "query": title, "year": year or None},
                timeout=15
            )
            r.raise_for_status()
            results = r.json().get("results", [])
            if results:
                return self.get_movie_details(results[0]["id"])
        except Exception as e:
            print(f"TMDb search failed {title}: {e}")
        return None

    def get_movie_details(self, movie_id):
        try:
            r = requests.get(f"{TMDB_API_BASE}/movie/{movie_id}", params={"api_key": self.api_key}, timeout=15)
            return r.json() if r.status_code == 200 else None
        except Exception as e:
            print(f"TMDb details failed {movie_id}: {e}")
        return None

    def get_providers(self, movie_id):
        try:
            r = requests.get(f"{TMDB_API_BASE}/movie/{movie_id}/watch/providers", params={"api_key": self.api_key}, timeout=15)
            data = r.json()
            return [p["provider_name"] for p in data.get("results", {}).get(self.country, {}).get("flatrate", [])]
        except Exception as e:
            print(f"Provider lookup failed {movie_id}: {e}")
        return []

    def enrich_film(self, film):
        movie = self.search_movie(film["title"], film.get("year"))
        if movie:
            film["tmdb_id"] = str(movie.get("id",""))
            film["overview"] = str(movie.get("overview",""))
            film["genres"] = ", ".join([g["name"] for g in movie.get("genres",[])])
            film["runtime"] = movie.get("runtime")
            poster = movie.get("poster_path")
            film["poster_url"] = f"https://image.tmdb.org/t/p/w500{poster}" if poster else ""
            film["providers"] = ", ".join(self.get_providers(movie.get("id"))) or ""
        time.sleep(RATE_LIMIT_DELAY)
        return film
