import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from spacy.language import Language
import logging

logger = logging.getLogger(__name__)

# Load the medium spaCy model
nlp = spacy.load("en_core_web_lg")

# Define custom entity labels for resume parsing
RESUME_LABELS = ["SKILL", "EXPERIENCE", "EDUCATION"]

# List of skills
skills_list = ["Python", "Machine Learning", "Data Analysis", "SQL", "JavaScript"]

# Create a PhraseMatcher for skills
skill_matcher = PhraseMatcher(nlp.vocab)
skill_patterns = [nlp(skill) for skill in skills_list]
skill_matcher.add("SKILL", skill_patterns)

# List of education degrees
education_degrees = ["Bachelor of Science", "Master of Arts", "PhD", "Doctorate"]

# Create a PhraseMatcher for education degrees
education_matcher = PhraseMatcher(nlp.vocab)
education_patterns = [nlp(education) for education in education_degrees]
education_matcher.add("EDUCATION", education_patterns)

# Define the custom component
@Language.component("custom_entity_extractor")
def custom_entity_extractor(doc):
    # Apply the skill matcher
    matches = skill_matcher(doc)
    new_ents = []
    for match_id, start, end in matches:
        span = Span(doc, start, end, label="SKILL")
        # Check for overlaps manually
        if not any((span.start < ent.end and span.end > ent.start) for ent in new_ents):
            new_ents.append(span)
    
    # Apply the education matcher
    matches = education_matcher(doc)
    for match_id, start, end in matches:
        span = Span(doc, start, end, label="EDUCATION")
        # Check for overlaps manually
        if not any((span.start < ent.end and span.end > ent.start) for ent in new_ents):
            new_ents.append(span)
    
    # Add new entities to the document
    doc.ents = list(doc.ents) + new_ents
    return doc

# Add the custom component to the pipeline
nlp.add_pipe("custom_entity_extractor", after="ner")

def parse_resume(text):
    """
    Parses resume text using spaCy and extracts structured data.
    """
    if not isinstance(text, str):
        raise ValueError("Input to parse_resume must be a string.")

    doc = nlp(text)
    parsed_data = {
        "skills": [],
        "experience": [],
        "education": []
    }

    # Extract entities
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            parsed_data["skills"].append(ent.text)
        elif ent.label_ == "EXPERIENCE":
            parsed_data["experience"].append(ent.text)
        elif ent.label_ == "EDUCATION":
            parsed_data["education"].append(ent.text)

    return parsed_data