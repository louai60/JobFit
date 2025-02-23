import spacy
from spacy.training import Example
import json

# Load pre-trained model
nlp = spacy.load("en_core_web_lg")

# Add custom labels to NER
for label in ["SKILL", "EXPERIENCE", "EDUCATION"]:
    nlp.get_pipe("ner").add_label(label)

# Load training data
with open('data/train.json', 'r') as f:
    TRAIN_DATA = json.load(f)

# Disable other pipeline components
with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != "ner"]):
    optimizer = nlp.create_optimizer()
    for epoch in range(10):
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses, sgd=optimizer)
        print(f"Epoch {epoch + 1}, Losses: {losses}")

# Save the fine-tuned model
nlp.to_disk("models/fine_tuned_model")