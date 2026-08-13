# Speech Recognition AI Chatbot

> A Python-based voice assistant prototype that converts speech to text, classifies user commands with a trained intent model, generates spoken responses, opens web services, and demonstrates home-automation and voice-commerce interactions.

## Project Overview

This project was developed as a Python voice-assistant / chatbot prototype inspired by Alexa-style interaction. The assistant accepts voice input, converts it to text, identifies the user's intent, and performs an action or generates a response.

The available resume material confirms the original project used **Python, SpeechRecognition, PyAudio and NLTK**, included conversational flows, and used a training dataset to improve natural-language understanding. The current repository is a clean reconstruction because the original source code was lost.

## Features

- Speech-to-text using `SpeechRecognition`
- Microphone input through `PyAudio`
- Intent classification using an NLTK Naive Bayes model
- Text-to-speech using `pyttsx3`
- Conversational responses
- Open YouTube, Google and Wikipedia
- Time and date queries
- Home-automation prototype for light and fan commands
- Voice-commerce / product catalog prototype
- JSON training dataset for intents
- Confidence threshold before executing commands

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| SpeechRecognition | Speech-to-text |
| PyAudio | Microphone input |
| NLTK | Tokenization and intent classification |
| Naive Bayes | Lightweight trained intent model |
| pyttsx3 | Text-to-speech |
| Webbrowser | Web-service integration |
| JSON | Training data and product catalog |
| HTML/CSS/JavaScript | Browser commerce prototype |

## System Flow

```text
Microphone
    ↓
Speech Recognition
    ↓
Recognized Text
    ↓
NLTK Tokenization
    ↓
Intent Classification
    ↓
Action / Response
    ├── Spoken response
    ├── Open web services
    ├── Home automation prototype
    └── Product / commerce demo
```

## Example Commands

### General

```text
Hello
What time is it?
What's today's date?
What can you do?
Goodbye
```

### Web

```text
Open YouTube
Open Google
Open Wikipedia
```

### Home Automation

```text
Turn on the light
Turn off the light
Turn on the fan
Turn off the fan
Control my home
```

The included automation layer is a software prototype that maintains simulated device states. It can later be connected to a real IoT controller or dashboard.

### Voice Commerce

```text
Show products
Find products
Search products
```

A small product catalog and browser demo are included to demonstrate how voice commands can be connected to an e-commerce-style interaction.

## Training the Intent Model

Training examples are stored in:

```text
data/intents.json
```

Train the model with:

```bash
python assistant/train_model.py
```

This creates a local trained model:

```text
models/intent_classifier.pkl
```

The classifier uses NLTK tokenization and a Naive Bayes model over bag-of-words features. More example phrases can be added to `intents.json` and the model retrained.

## Installation

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Train the model:

```bash
python assistant/train_model.py
```

Run the assistant:

```bash
python assistant/voice_assistant.py
```

A working microphone and internet connection are required for the default speech-recognition backend.

## Project Structure

```text
speech-recognition-ai-chatbot/
│
├── assistant/
│   ├── train_model.py
│   ├── voice_assistant.py
│   └── test_intents.py
│
├── data/
│   ├── intents.json
│   └── products.json
│
├── web_demo/
│   └── index.html
│
├── docs/
│   └── architecture.md
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Limitations

This is an educational prototype, not a production Alexa replacement.

- Speech recognition depends on microphone quality and environment.
- The default recognition backend requires internet access.
- The training dataset is intentionally small.
- Commands outside the training examples may not classify correctly.
- Home automation is simulated unless connected to real hardware.
- The e-commerce component is a demonstration catalog, not a payment/order platform.

## Future Improvements

- Wake-word detection
- Larger and more diverse training dataset
- Multilingual speech recognition
- Modern NLU / transformer-based intent detection
- MQTT/REST integration with real IoT devices
- Authentication and authorization for automation commands
- Real product database and search APIs
- Cart, order and payment workflows
- Web or mobile deployment
- Automated tests and CI

## Academic / Portfolio Context

**Project:** Speech Recognition AI Chatbot System  
**Primary language:** Python  
**Project type:** Voice assistant / Natural Language Processing prototype

## Author

**Nithesh S**  
B.E. Electronics & Communication Engineering

GitHub: `nitheshstech-dev`

LinkedIn: `linkedin.com/in/nithesh-s-699733368`

## Note on Reconstruction

The original project source code was lost. This repository is a portfolio reconstruction based on the project description available in the author's resume and the author's recollection of the original prototype. Features that cannot be verified from the original source are presented as reconstruction features rather than as the exact historical implementation.
