from __future__ import annotations

import json
import os
import pickle
import random
import webbrowser
from datetime import datetime
from pathlib import Path
from threading import Thread

import nltk
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize

BASE = Path(__file__).resolve().parents[1]
INTENTS_PATH = BASE / "data" / "intents.json"
PRODUCTS_PATH = BASE / "data" / "products.json"
MODEL_PATH = BASE / "models" / "intent_classifier.pkl"

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 175)

intents = json.loads(INTENTS_PATH.read_text(encoding="utf-8"))["intents"]

if not MODEL_PATH.exists():
    raise FileNotFoundError("Train the model first: python assistant/train_model.py")

with MODEL_PATH.open("rb") as f:
    model = pickle.load(f)

classifier = model["classifier"]
vocabulary = model["vocabulary"]

home_state = {"light": False, "fan": False}
HOME_AUTOMATION_URL = os.getenv("HOME_AUTOMATION_URL", "")


def speak(text: str) -> None:
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower().strip()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand that.")
    except sr.RequestError:
        speak("The speech recognition service is unavailable.")
    return ""


def features(text: str) -> dict:
    tokens = set(word.lower() for word in word_tokenize(text))
    return {word: word in tokens for word in vocabulary}


def classify(text: str) -> tuple[str, float]:
    distribution = classifier.prob_classify(features(text))
    tag = distribution.max()
    return tag, distribution.prob(tag)


def get_intent(tag: str) -> dict:
    return next(item for item in intents if item["tag"] == tag)


def home_automation(text: str) -> str:
    if "light" in text and ("turn on" in text or "switch on" in text):
        home_state["light"] = True
        return "The prototype light is now on."
    if "light" in text and ("turn off" in text or "switch off" in text):
        home_state["light"] = False
        return "The prototype light is now off."
    if "fan" in text and ("turn on" in text or "switch on" in text):
        home_state["fan"] = True
        return "The prototype fan is now on."
    if "fan" in text and ("turn off" in text or "switch off" in text):
        home_state["fan"] = False
        return "The prototype fan is now off."

    if HOME_AUTOMATION_URL:
        webbrowser.open(HOME_AUTOMATION_URL)
        return "Opening the configured home automation dashboard."

    return f"Light is {'on' if home_state['light'] else 'off'} and fan is {'on' if home_state['fan'] else 'off'}."


def product_search(text: str) -> str:
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    query_words = {w for w in word_tokenize(text.lower()) if len(w) > 2}
    matches = []
    for product in products:
        haystack = f"{product['name']} {product['category']}".lower()
        if any(word in haystack for word in query_words):
            matches.append(product)
    matches = matches or products[:3]
    return " | ".join(f"{p['name']} — ₹{p['price']}" for p in matches[:5])


def handle(tag: str, text: str) -> bool:
    if tag == "greeting":
        speak(random.choice(get_intent(tag)["responses"]))
    elif tag == "goodbye":
        speak(random.choice(get_intent(tag)["responses"]))
        return False
    elif tag == "thanks":
        speak(random.choice(get_intent(tag)["responses"]))
    elif tag == "time":
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}.")
    elif tag == "date":
        speak(f"Today is {datetime.now().strftime('%A, %d %B %Y')}.")
    elif tag == "youtube":
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube.")
    elif tag == "google":
        webbrowser.open("https://www.google.com/")
        speak("Opening Google.")
    elif tag == "wikipedia":
        webbrowser.open("https://www.wikipedia.org/")
        speak("Opening Wikipedia.")
    elif tag == "home_automation":
        speak(home_automation(text))
    elif tag == "ecommerce":
        result = product_search(text)
        print(f"Products: {result}")
        speak("Here are the matching products.")
    elif tag == "help":
        speak(get_intent(tag)["responses"][0])
    else:
        speak("That command is not implemented in this prototype yet.")
    return True


def main() -> None:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    speak("Voice assistant started. Say help for supported commands, or say exit to stop.")

    while True:
        text = listen()
        if not text:
            continue
        tag, confidence = classify(text)
        print(f"Intent: {tag} | confidence: {confidence:.2f}")
        if confidence < 0.45:
            speak("I'm not confident I understood that. Please try again.")
            continue
        if not handle(tag, text):
            break


if __name__ == "__main__":
    main()
