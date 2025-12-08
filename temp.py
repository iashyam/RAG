import json
from pathlib import Path

search_query = "Avatar"


with open("data/movies.json", "r", encoding="utf-8") as f:
    total_json = f.read()

movies_json = json.loads(total_json)
movies =  movies_json["movies"]


for movie in movies:
    movie_titles: str = movie['title']
    if search_query.lower() in movie_titles.lower():
        print(movie_titles)