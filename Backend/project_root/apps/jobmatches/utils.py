import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_resume(resume_text):
    # Process the text with spaCy
    doc = nlp(resume_text)
    # Extract skills, experience, etc.
    skills = [token.text for token in doc if token.ent_type_ == "SKILL"]  # Assuming 'SKILL' is a custom entity type you trained or predefined
    experience = [ent.text for ent in doc.ents if ent.label_ == "EXPERIENCE"]  # Example for extracting experience
    # You can expand this function to extract more entities as needed
    return {
        "skills": skills,
        "experience": experience
    }

