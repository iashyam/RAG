from search_json import search_movies
from pathlib import Path
import string

def search_hanlder(query: str):
    results = search_movies(file=Path("data/movies.json"), search_query=query)
    print(f"Searching for: {query}")

    for i, movie in enumerate(results):
        if i==5:
            return
        print(f"{i+1}. {movie}")
