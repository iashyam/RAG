import json
from pathlib import Path
from helpers import *

def get_stop_words(file: Path) -> list[str]:
    ''' you know what it does'''
    if not file.exists():
        raise FileNotFoundError(f"file {file} doesn't exists")
    
    with open(file, "r", encoding="utf-8") as f:
        stop_words = []
        for line in f:
            stop_words.append(line.strip())
        return stop_words


stop_words = get_stop_words(Path("data/stop_words.txt"))

def load_json(file: Path)->dict:
    """loads the json file, returns and error if not exist."""
    
    if not file.exists():
        raise FileNotFoundError(f"file {file} doesn't exists")

    with open("data/movies.json", "r", encoding="utf-8") as f:
        total_json = f.read()

    movies_json = json.loads(total_json)
    return movies_json


def search_movies(file: Path, search_query: str) -> list[str]:
    """
    searches a query in the json file loacated file. Parses the movies
    returns a list of movies which have the search_query in their title. 
    """

    total_json = load_json(file)
    movies =  total_json["movies"]
 
    search_query_tokens = tokenise(remove_stop_words(search_query, stop_words=stop_words))
    matched_movies = []
    for movie in movies:
        movie_titles: str = movie['title']
        for token in search_query_tokens:
            if token in simplify(movie_titles):
                matched_movies.append(movie_titles)
                break

    return matched_movies