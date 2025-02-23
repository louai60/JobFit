import spacy
from spacy.training import Example
import json

# Load fine-tuned model
nlp = spacy.load("models/fine_tuned_model")

# Load validation data
with open('data/validate.json', 'r') as f:
    VALID_DATA = json.load(f)

# Evaluate the model
for text, annotations in VALID_DATA:
    doc = nlp(text)
    example = Example.from_dict(doc, annotations)
    nlp.evaluate([example])