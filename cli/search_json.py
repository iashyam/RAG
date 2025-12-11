import json
from pathlib import Path
from helpers import *
import pickle
from tqdm import tqdm
import math
from collections import Counter
import os

class InvertedIndex:

    def __init__(self):
        
        self.index = {}
        self.docmap = {}
        self.index_path = Path("cache/index.pkl")
        self.docma_path = Path("cache/docmap.pkl")
        self.term_frequencies_path = Path("cache/term_frequencies.pkl")
        self.term_frequencies: dict[int, Counter] = {}

    def __add_document(self, doc_id, text):
        
        tokenised_text = tokenise(text)
        self.term_frequencies[doc_id] = Counter()
        for token in tokenised_text:
            if token not in self.docmap:
                self.docmap[token] = []
            if doc_id not in self.docmap[token]:
                self.docmap[token].append(doc_id)
            self.term_frequencies[doc_id][token] += 1

    def get_idf(self, term):
        term = tokenise(term)
        if len(term)>1:
            raise Exception("there should be only one term")

        term = term[0]
        total_doc_count = len(self.index)
        term_match_doc_count = len(self.docmap[term])
        idf = math.log((total_doc_count + 1) / (term_match_doc_count + 1))
        return idf

    def get_bm_25_idf(self, term: str)->float:
        term = tokenise(term)
        if len(term)>1:
            raise Exception("there should be only one term")

        term = term[0]

        N = len(self.index)
        df = len(self.docmap[term])
        IDF = math.log((N - df + 0.5) / (df + 0.5) + 1)

        return IDF



    def get_documents(self, term):

        term = simplify(term)
        if term not in self.docmap.keys():
            return []
        return sorted(self.docmap[term])

    def get_tf(self, doc_id, term):
        term = tokenise(term)
        if len(term)>1:
            raise Exception("there should be only one term")

        term = term[0]
        value = self.term_frequencies[doc_id].get(term)
        return value if value else "O"


    def build(self, movie_data_path: Path):

        json = load_json(movie_data_path)
        movies = json["movies"]

        for movie in ( bar := tqdm(movies)):
            bar.set_description_str("Building Index")
            text = f"{movie["title"]} {movie["description"]}"
            self.__add_document(movie['id'], text)
            self.index[movie['id']] = movie

    def save(self):
        
        #make cache dir if not exists
        if not os.path.exists("cache"):
            os.mkdir("cache")

        with open(self.index_path, "wb") as f:
            pickle.dump(self.index,f)
        with open(self.docma_path, "wb") as f:
            pickle.dump(self.docmap,f)
        with open(self.term_frequencies_path, "wb") as f:
            pickle.dump(self.term_frequencies,f)

    def load(self):
        if not(self.index_path.exists() \
              and self.docma_path.exists() \
              and self.term_frequencies_path.exists()):
            raise FileExistsError("path to cache file wrong check!")
        
        with open(self.index_path, "rb") as file:
            self.index = pickle.load(file)

        with open(self.docma_path, "rb") as file:
            self.docmap = pickle.load(file)

        with open(self.term_frequencies_path, "rb") as file:
            self.term_frequencies = pickle.load(file)
    

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