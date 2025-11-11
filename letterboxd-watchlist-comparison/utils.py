import re

def clean_year(year):
    year = str(year).strip().lower()
    if year == 'nan' or not year:
        return ''
    return year[:-2] if year.endswith('.0') else year

def get_film_key(film):
    return (film.get('title', '').strip(), clean_year(film.get('year', '')))

def parse_runtime(runtime_str):
    try:
        runtime_str = runtime_str.strip()
        return int(float(runtime_str)) if runtime_str else None
    except ValueError:
        return None
