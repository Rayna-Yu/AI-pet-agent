from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Tuple, Optional, Any
import json, math, re, textwrap, random, os, sys
from collections import Counter, defaultdict

def normalize_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten RescueGroups API response and create a searchable text blob."""
    
    attr = entry.get("attributes", {})

    name = attr.get("animalName", "")
    species = attr.get("animalSpecies", "")
    breed = attr.get("animalBreed", "")
    age = attr.get("animalAgeString", "")
    sex = attr.get("animalSex", "")
    desc = attr.get("animalDescriptionPlain", "")
    location = attr.get("animalLocation", "")

    # title for ranking
    title = f"{name} - {species}"

    # text blob used for TF-IDF
    text = (
        f"name {name} "
        f"species {species} "
        f"breed {breed} "
        f"age {age} "
        f"sex {sex} "
        f"location {location} "
        f"description {desc}"
    )

    normalized = {
        "id": entry.get("id"),
        "name": name,
        "species": species,
        "breed": breed,
        "age": age,
        "sex": sex,
        "location": location,
        "description": desc,
        "pictures": attr.get("animalPictures", []),

        # internal search fields
        "title": title,
        "text": text,
    }

    return normalized

# Load your file here
with open("toy_corpus.json", "r") as f:
    raw_json = json.load(f)

# RescueGroups wraps results in "data": [...]
raw_list = raw_json["data"]

# Normalize all animals
CORPUS = [normalize_entry(e) for e in raw_list]

# Tokenize the document into words
def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9']+", text.lower())

# et all the words of each document in the corpus
DOC_TOKENS = [tokenize(d["title"] + " " + d["text"]) for d in CORPUS]

# Get all the words from the corpus
VOCAB = sorted(set(t for doc in DOC_TOKENS for t in doc))


# Compute term frequency (TF) for each doc
def compute_tf(tokens: List[str]) -> Dict[str, float]:

    counts = defaultdict(int)
    for token in tokens:
        counts[token] += 1

    length = max(1, len(tokens))
    
    return {token: counts[token] / length for token in counts}



# Compute the document frequency across corpus: how many docs does a word appear?
def compute_df(doc_tokens: List[List[str]]) -> Dict[str, float]:
    df = defaultdict(int)
    for tokens in doc_tokens:
        for token in set(tokens):
            df[token] += 1
    return df

# Compute the inverse document frequency (higher for rarer terms), in which we use a smoothed variant
DF = compute_df(DOC_TOKENS)
N_DOC = len(DOC_TOKENS)
IDF = {t: math.log((N_DOC + 1) / (DF[t] + 0.5)) + 1 for t in VOCAB} 


# Compute TF-IDF vectors for each document, which is the product between
def tfidf_vector(tokens: List[str]) -> Dict[str, float]:
    tf = compute_tf(tokens)
    vec = {t: tf[t] * IDF.get(t, 0.0) for t in tf}
    return vec

DOC_VECS = [tfidf_vector(tokens) for tokens in DOC_TOKENS]


# Compute the cosine similarity for the search
def cosine(a: Dict[str, float], b: Dict[str, float]) -> float:

    if not a or not b:
        return 0.0

    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in set(a) | set(b))
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    return dot / (na * nb + 1e-12)


# Implement a search method based on the cosine similarity, which finds the documents with the highest similarity scores as the top-k search results.
def search_pets(query: str, k: int = 3) -> List[Dict[str, Any]]:
    qvec = tfidf_vector(tokenize(query))
    scored = [(cosine(qvec, v), i) for i, v in enumerate(DOC_VECS)]
    scored.sort(reverse=True)
    
    results = []
    for score, idx in scored[:k]:
        d = CORPUS[idx].copy()
        d["score"] = float(score)
        results.append(d)
    return results

# Integrate the search method as a tool
def tool_search(query: str, k: int = 3) -> Dict[str, Any]:
    hits = search_pets(query, k=k)
    return {
        "tool": "search",
        "query": query,
        "results": [
            {
                "id": h["id"],
                "name": h["name"],
                "species": h["species"],
                "breed": h["breed"],
                "age": h["age"],
                "sex": h["sex"],
                "location": h["location"],
                "score": h["score"],
                "snippet": h["description"][:200] + ("..." if len(h["description"]) > 200 else "")
            }
            for h in hits
        ],
    }

TOOLS = {
    "search": {
        "schema": {"query": "str", "k": "int? (default=3)"},
        "fn": tool_search
    },
    "finish": {
        "schema": {"answer": "str"},
        "fn": lambda answer: {"tool": "finish", "answer": answer}
    }
}