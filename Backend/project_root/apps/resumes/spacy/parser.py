from .pdf_extractor import extract_text_from_pdf
from .spacy_parser import parse_resume_with_spacy
import logging

logger = logging.getLogger(__name__)

def parse_resume(pdf_path):
    """
    Parses a resume PDF and extracts structured data.
    """
    try:
        # Extract text from the PDF
        logger.info(f"Extracting text from PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        if not text:
            logger.warning("No text extracted from the PDF.")
            return {
                "skills": [],
                "experience": [],
                "education": []
            }

        # Parse the extracted text using spaCy
        logger.info("Parsing the extracted text with spaCy.")
        parsed_data = parse_resume_with_spacy(text)

        return parsed_data

    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}", exc_info=True)
        return {
            "skills": [],
            "experience": [],
            "education": []
        }