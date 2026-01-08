from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import os
from tqdm import tqdm
from typing import List
import numpy as np
from helpers import similarity

class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents: List[dict] = None
        self.embeddings: np.ndarray = None
        self.document_map: Dict[int, dict] = {}

    def generate_embeddings(self, sentence: str) -> List[float]:
        return self.model.encode([sentence])[0]

    def build_embeddings(self, documents: List[dict]):
        self.documents = documents
        self.embeddings = np.zeros((len(documents), self.model.get_sentence_embedding_dimension()))
        for i, doc in enumerate(tqdm(documents)):
            self.document_map[i] = doc  
            string_document = f"{doc['title']} {doc['description']}"
            self.embeddings[i] = self.model.encode(string_document, convert_to_numpy=True)
        
        #save embeddings in cache
        np.save("cache/embeddings.npy", self.embeddings)
        return self.embeddings
    
    def load_or_create_embeddings(self, documents: List[dict]):
        self.documents = documents
        self.document_map = {i: doc for i, doc in enumerate(documents)}
        if os.path.exists("cache/embeddings.npy"):
            self.embeddings = np.load("cache/embeddings.npy")
            if self.embeddings.shape[0] == len(documents):
                return self.embeddings
        return self.build_embeddings(documents)

    def calculate_similarities(self, query: str, limit: int = 5):
        if self.embeddings is None:
            raise ValueError("Embeddings not loaded. Please load or create embeddings first.")
        query_embedding = self.generate_embeddings(query)
        similarities = [similarity(query_embedding, doc_embedding) for doc_embedding in self.embeddings]
        similarities = np.array(similarities)
        return similarities

def verify_model():
    search = SemanticSearch()
    print(f"Model Loaded {search.model}")
    print(f"Max sentence length: {search.model.max_seq_length}")

def embed(sentence: str) -> List[float]:
    search = SemanticSearch()
    embedding = search.generate_embeddings(sentence)
    print(f"Text: {sentence}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")
    return embedding

def load_json(file: Path)->dict:
    """loads the json file, returns and error if not exist."""
    
    if not file.exists():
        raise FileNotFoundError(f"file {file} doesn't exists")

    with open(file, "r", encoding="utf-8") as f:
        total_json = f.read()

    movies_json = json.loads(total_json)
    return movies_json

def verify_embeddings():
    search = SemanticSearch()
    json_data = load_json(Path("data/movies.json"))
    documents = json_data['movies']
    embeddings = search.load_or_create_embeddings(documents)
    print(f"Number of docs:   {len(documents)}")
    print(f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")

def embed_query_text(query: str):
    search = SemanticSearch()
    embedding = search.generate_embeddings(query)
    print(f"Query: {query}")
    print(f"First 5 dimensions: {embedding[:5]}")
    print(f"Shape: {embedding.shape}")
    return embedding

def search(query: str, limit: int = 5):
    json_data = load_json(Path("data/movies.json"))
    documents = json_data['movies']
    search = SemanticSearch()
    search.load_or_create_embeddings(documents)
    similarities = search.calculate_similarities(query, limit)
    top_indices = np.argsort(similarities)[::-1][:limit]
    for i, idx in enumerate(top_indices):
        print(f"{i+1}. {search.documents[idx]['title']} (score : {similarities[idx]})")
        print(search.documents[idx]['description'])
        print("\n")


if __name__ == "__main__":
    search("funny bear movies")
