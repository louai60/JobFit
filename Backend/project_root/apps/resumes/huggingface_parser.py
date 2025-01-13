import requests
import logging
import re
from django.conf import settings

# Initialize logger
logger = logging.getLogger(__name__)

# HuggingFace API URL and Token
HF_API_URL = "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english"
HF_API_TOKEN = settings.HUGGINGFACE_API_TOKEN

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def preprocess_resume(text):
    """Preprocess resume to remove noise like emails and links."""
    text = re.sub(r'\S+@\S+', '', text)  # Remove emails
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[|]', '', text)  # Remove unnecessary symbols like '|'
    return text.strip()

def get_entities_from_api(resume_text):
    """Calls HuggingFace API for NER and returns the result."""
    try:
        response = requests.post(
            HF_API_URL, 
            headers=headers,
            json={"inputs": resume_text}
        )

        if response.status_code == 200:
            logger.debug(f"NER API Response: {response.json()}")
            return response.json()
        else:
            logger.error(f"Error calling HuggingFace API: {response.status_code}, {response.text}")
            return {"error": f"Failed to process resume: {response.text}"}
    except Exception as e:
        logger.error(f"Error during HuggingFace API request: {str(e)}")
        return {"error": str(e)}

def clean_and_categorize_entities(entities):
    """Clean and organize entities into categories like skills, tools, projects, etc."""
    categories = {
        "skills": [],
        "tools": [],
        "projects": [],
        "experience": []
    }

    # Define keyword-based rules for categorization
    skill_keywords = {"javascript", "python", "react", "angular", "java", "html", "css"}
    tool_keywords = {"git", "jira", "spring boot", "mongodb", "docker", "kubernetes"}
    project_indicators = {"project", "system", "platform"}
    experience_indicators = {"tunis", "tunisia", "intern", "developer"}

    for entity in entities:
        word = entity.get("word", "").replace("##", "").strip()  # Clean word
        label = entity.get("entity_group", "").lower()

        if not word:  # Skip empty words
            continue

        # Categorize based on entity label and keyword rules
        if label == "misc" or word.lower() in skill_keywords:
            categories["skills"].append(word)
        elif label == "org" or word.lower() in tool_keywords:
            categories["tools"].append(word)
        elif any(indicator in word.lower() for indicator in project_indicators):
            categories["projects"].append(word)
        elif label in {"loc", "per", "org"} or any(indicator in word.lower() for indicator in experience_indicators):
            categories["experience"].append(word)

    # Deduplicate and clean up entries
    for key in categories:
        categories[key] = list(set(categories[key]))
        # Remove irrelevant short words or duplicates
        categories[key] = [word for word in categories[key] if len(word) > 2]

    return categories

def parse_resume_with_api(resume_text):
    """Parse resume text using HuggingFace API and organize entities into categories."""
    try:
        # Preprocess the resume text
        clean_text = preprocess_resume(resume_text)
        logger.info("Preprocessed Resume Text Successfully")

        # Get entities from HuggingFace API
        api_response = get_entities_from_api(clean_text)

        if "error" in api_response:
            logger.error("NER API returned an error.")
            return {"error": api_response["error"]}

        if not isinstance(api_response, list):
            logger.error(f"Unexpected NER API response format: {api_response}")
            return {"error": "Unexpected API response format"}

        # Clean and categorize NER entities
        categorized_entities = clean_and_categorize_entities(api_response)
        logger.info(f"Categorized Parsed Data: {categorized_entities}")

        return {"parsed_data": categorized_entities}

    except Exception as e:
        logger.error(f"Error parsing resume with API: {str(e)}")
        return {"error": str(e)}
