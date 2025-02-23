import spacy

# Load fine-tuned model
nlp = spacy.load("models/fine_tuned_model")

def parse_resume(text):
    doc = nlp(text)
    parsed_data = {
        "skills": [],
        "experience": [],
        "education": []
    }
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            parsed_data["skills"].append(ent.text)
        elif ent.label_ == "EXPERIENCE":
            parsed_data["experience"].append(ent.text)
        elif ent.label_ == "EDUCATION":
            parsed_data["education"].append(ent.text)
    return parsed_data