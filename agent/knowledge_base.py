from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Tuple, Optional, Any
import json, math, re, textwrap, random, os, sys
import math
from collections import Counter, defaultdict

# A toy corpus of pet facts
CORPUS = [
    {
        "id": "doc1",
        "title": "Dog Daily Exercise",
        "text": (
            "Most dogs need at least 30 minutes to 2 hours of exercise per day, depending on breed and age. "
            "Daily walks, playtime, and mental stimulation help maintain their physical and mental health."
        ),
    },
    {
        "id": "doc2",
        "title": "Cat Nutrition Basics",
        "text": (
            "Cats are obligate carnivores and require a diet high in protein. "
            "A balanced diet includes wet food or high-quality dry food, with occasional treats in moderation."
        ),
    },
    {
        "id": "doc3",
        "title": "Puppy Socialization",
        "text": (
            "Puppies benefit from early socialization between 3 and 14 weeks of age. "
            "Introduce them to different people, animals, and environments to promote confidence and reduce fearfulness."
        ),
    },
    {
        "id": "doc4",
        "title": "Common Dog Health Issues",
        "text": (
            "Some common health issues in dogs include ear infections, skin allergies, obesity, and dental problems. "
            "Regular check-ups and preventive care help detect and manage these conditions."
        ),
    },
    {
        "id": "doc5",
        "title": "Cat Litter Training",
        "text": (
            "Most cats naturally use a litter box, but kittens may need guidance. "
            "Keep the litter box clean, in a quiet location, and show kittens where it is after meals and naps."
        ),
    },
    {
        "id": "doc6",
        "title": "Dog Grooming Tips",
        "text": (
            "Regular grooming keeps dogs healthy and comfortable. Brush coats to prevent matting, trim nails, and clean ears. "
            "Bathing frequency depends on breed and activity level."
        ),
    },
    {
        "id": "doc7",
        "title": "Signs of Stress in Cats",
        "text": (
            "Cats may show stress through hiding, over-grooming, loss of appetite, or aggression. "
            "Providing a safe environment and enrichment can help reduce stress."
        ),
    },
    {
        "id": "doc8",
        "title": "Feeding Schedule for Dogs",
        "text": (
            "Adult dogs are usually fed twice daily, while puppies may need three to four small meals per day. "
            "Maintain portion control to prevent obesity."
        ),
    },
    {
        "id": "doc9",
        "title": "Basic Dog Training Commands",
        "text": (
            "Important commands for dogs include sit, stay, come, and leash walking. "
            "Use positive reinforcement techniques such as treats, praise, and consistency."
        ),
    },
    {
        "id": "doc10",
        "title": "Traveling Safely with Pets",
        "text": (
            "When traveling with pets, ensure they are secured in carriers or seat belts. "
            "Provide water, take breaks for exercise, and never leave pets unattended in vehicles."
        ),
    },
]


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
def search_corpus(query: str, k: int = 3) -> List[Dict[str, Any]]:
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
    hits = search_corpus(query, k=k)
    # Return a concise, citation-friendly payload
    return {
        "tool": "search",
        "query": query,
        "results": [
            {"id": h["id"], "title": h["title"], "snippet": h["text"][:240] + ("..." if len(h["text"]) > 240 else "")}
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