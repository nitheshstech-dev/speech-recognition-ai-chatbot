from train_model import features, classifier

samples = [
    "open youtube",
    "what time is it",
    "turn on the light",
    "show products",
]

for text in samples:
    distribution = classifier.prob_classify(features(text))
    print(f"{text!r} -> {distribution.max()} ({distribution.prob(distribution.max()):.2f})")
