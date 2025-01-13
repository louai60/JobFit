import requests
import logging
from django.conf import settings

# Hugging Face API URL and your API Token
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_TOKEN = settings.HUGGINGFACE_API_TOKEN

# Headers for API authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def summarize_text(text):
    """
    Summarizes the provided resume text using Hugging Face's BART model for summarization.
    The focus is on skills, tools, and education.
    """
    prompt = f"""
    "Summarize the resume text with the following structure:
    Skills: List key programming languages, tools, and frameworks mentioned.
    Education: Include details about degrees, institutions, certifications, and graduation years.
    Professional Experience: Summarize job roles, company names, technologies used, and key responsibilities.
    Projects: Highlight major projects, technologies used, and achievements.
    Resume Text:
    {text}
    """

    payload = {
        "inputs": prompt,
        "parameters": {"min_length": 50, "max_length": 200}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            summary = response.json()[0]["summary_text"]
            logging.info(f"Summarized Text: {summary}")
            return summary
        else:
            raise ValueError(f"Error in summarizing: {response.text}")
    except Exception as e:
        return str(e)
