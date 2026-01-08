from keyword_search_utils import search_movies, InvertedIndex, BM25_B, BM25_K1
from pathlib import Path
from helpers import tokenise
import string

movies_file_path = Path("data/movies.json")

def search_hanlder(query: str):
    print(f"Searching for: {query}")

    inv_idx = InvertedIndex()
    try:
        inv_idx.load()
    except Exception as e:
        print(e)
        exit(0)
  
    results = list()
    for token in tokenise(query):
        results.extend(inv_idx.get_documents(token))
        if len(results)>5:
            break

    for i, movie in enumerate(results):
        if i==5:
            return
        print(f"{i+1}. {inv_idx.index[movie]["title"]}")

def build_handler():

    inv_idx = InvertedIndex()
    inv_idx.build(movies_file_path)
    inv_idx.save()

    docs = inv_idx.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")

def tf_handler(doc_id, term):
    inv_idx = InvertedIndex()

    try:
        inv_idx.load()
        tf = inv_idx.get_tf(doc_id, term)
        print(f"Term frequency for term {term}: {tf}")
    except Exception as e:
        print(e); exit(1)

def bm25tf_handler(doc_id, term, k1=BM25_K1, b=BM25_B):
    inv_idx = InvertedIndex()

    try:
       inv_idx.load()
       tf_component = inv_idx.get_bm25_tf(doc_id, term, b, k1)
       print(f"BM25 TF score of '{term}' in document '{doc_id}': {tf_component:.2f}")    

    except Exception as e:
        print(e); exit(1)

def idf_handler(term):

    inv_idx = InvertedIndex()
    try:
        inv_idx.load()
        idf = inv_idx.get_idf(term)
        print(f"Inverse document frequency of '{term}': {idf:.2f}")
    except Exception as e:
        print(e); exit(1)

def tf_idf_handler(doc_id, term):

    inv_idx = InvertedIndex()
    try:
        inv_idx.load()
        idf = inv_idx.get_idf(term)
        tf = inv_idx.get_tf(doc_id, term)
        tf_idf = tf * idf
        print(f"TF-IDF score of '{term}' in document '{doc_id}': {tf_idf:.2f}")
    except Exception as e:
        print(e); exit(1)


def bm25_handler(query, limit):
    inv_idx = InvertedIndex()
    try:
        inv_idx.load()
        sorted_doc = inv_idx.bm25_search(query)
        for i, (key, value) in enumerate(sorted_doc.items()):
            print(f"{i+1}. ({key}) {inv_idx.index[key]["title"]} - score {value:.2f}")
            if i>limit:
                break

    except Exception as e:
        print(e); exit(1)



def bm25idf_handler(term):
    inv_idx = InvertedIndex()
    try:
        inv_idx.load()
        idf = inv_idx.get_bm_25_idf(term)
        print(f"TF-IDF score of '{term}': {idf:.2f}")
    except Exception as e:
        print(e); exit(1)


def chunk_handler(text, chunk_size: int = 200, overlap: int = 0):
    words = text.split()
    chunked_text = []
    for i in range(0, len(words), chunk_size):
        if i>overlap:
            chunked_text.append(" ".join(words[i-overlap:i+chunk_size-overlap]))
        else:
            chunked_text.append(" ".join(words[:i+chunk_size]))
    print(f"Chunking {len(text)} characters")
    for i, chunk in enumerate(chunked_text):
        print(f"{i+1}. {chunk}")
    return chunked_text