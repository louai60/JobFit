# resumes/spacy_parser.py
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

# Load the large spaCy model
nlp = spacy.load("en_core_web_lg")

# Define custom entity labels for resume parsing
RESUME_LABELS = ["SKILL", "EXPERIENCE", "EDUCATION"]

def parse_resume_with_spacy(text):
    """
    Parses resume text using spaCy and extracts structured data.
    """
    doc = nlp(text)

    # Initialize result dictionary
    parsed_data = {
        "skills": [],
        "experience": [],
        "education": []
    }

    # Extract entities
    for ent in doc.ents:
        if ent.label_ in RESUME_LABELS:
            if ent.label_ == "SKILL":
                parsed_data["skills"].append(ent.text)
            elif ent.label_ == "EXPERIENCE":
                parsed_data["experience"].append(ent.text)
            elif ent.label_ == "EDUCATION":
                parsed_data["education"].append(ent.text)

    # Add custom rule-based matching for skills (optional)
    skills = ["Python", "Machine Learning", "Data Analysis"]  # Add your skill list
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(skill) for skill in skills]
    matcher.add("SKILLS", None, *patterns)

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = Span(doc, start, end, label="SKILL")
        parsed_data["skills"].append(span.text)

    return parsed_data