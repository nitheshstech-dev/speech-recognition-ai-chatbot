import json
import pickle
import random
from pathlib import Path

import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "intents.json"
MODEL_DIR = BASE / "models"
MODEL_DIR.mkdir(exist_ok=True)

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
documents = []
vocabulary = set()

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = [token.lower() for token in word_tokenize(pattern)]
        vocabulary.update(tokens)
        documents.append((tokens, intent["tag"]))

vocabulary = sorted(vocabulary)


def features(tokens: list[str]) -> dict:
    token_set = set(tokens)
    return {word: (word in token_set) for word in vocabulary}


random.seed(42)
random.shuffle(documents)
dataset = [(features(tokens), tag) for tokens, tag in documents]
classifier = NaiveBayesClassifier.train(dataset)

with (MODEL_DIR / "intent_classifier.pkl").open("wb") as f:
    pickle.dump({"classifier": classifier, "vocabulary": vocabulary}, f)

print(f"Training examples: {len(dataset)}")
print(f"Vocabulary size: {len(vocabulary)}")
print("Model saved to models/intent_classifier.pkl")
