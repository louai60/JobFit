from PyPDF2 import PdfReader
import docx
import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)

# from PyMuPDF import fitz  

import pdfplumber

logger = logging.getLogger(__name__)

def extract_text_pdf(file):
    """Extract text from a PDF file using pdfplumber."""
    try:
        file.seek(0)  # Ensure the file pointer is at the beginning
        with pdfplumber.open(file) as pdf:
            text = []
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                else:
                    logger.warning(f"Page {page_num+1} did not contain extractable text.")
        
        extracted_text = "\n".join(text)

        if not extracted_text:
            raise ValueError("No text could be extracted from the PDF")

        logger.debug(f"----------------------------------------Extracted PDF Text-------------------------------------: {extracted_text}")
        logger.debug(f"PDF Extraction - Pages: {len(pdf.pages)}, Characters: {len(extracted_text)}")
        return extracted_text.strip()

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise


def extract_text_docx(file):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        logger.debug(f"Extracted DOCX Text: {text}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise

def extract_text_txt(file):
    """Extract text from a TXT file."""
    try:
        text = file.read().decode('utf-8')
        logger.debug(f"Extracted TXT Text: {text}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {str(e)}")
        raise

def extract_text_rtf_odt(file):
    """
    Extract text from RTF or ODT files using pandoc.
    Requires pandoc to be installed on the system.
    """
    try:
        # Create a temporary file to save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Use pandoc to convert the file to plain text
        result = subprocess.run(
            ['pandoc', '-f', 'odt' if file.name.endswith('.odt') else 'rtf', 
             '-t', 'plain', temp_file_path],
            capture_output=True,
            text=True
        )

        # Clean up the temporary file
        os.unlink(temp_file_path)

        if result.returncode != 0:
            raise Exception(f"Pandoc conversion failed: {result.stderr}")

        extracted_text = result.stdout.strip()
        logger.debug(f"Extracted RTF/ODT Text: {extracted_text}")
        return extracted_text

    except Exception as e:
        logger.error(f"Error extracting text from RTF/ODT: {str(e)}")
        raise

def extract_text_from_resume(file):
    """
    Main function to extract text from different file types.
    """
    try:
        file_name = file.name.lower()
        
        if file_name.endswith('.pdf'):
            return {'text': extract_text_pdf(file)}
        elif file_name.endswith('.docx'):
            return {'text': extract_text_docx(file)}
        elif file_name.endswith('.txt'):
            return {'text': extract_text_txt(file)}
        elif file_name.endswith('.rtf') or file_name.endswith('.odt'):
            return {'text': extract_text_rtf_odt(file)}
        else:
            error_msg = f"Unsupported file format: {file_name}"
            logger.error(error_msg)
            return {'error': error_msg}
            
    except Exception as e:
        logger.error(f"Failed to extract text from file {file.name}: {str(e)}")
        return {'error': f"Failed to extract text from file {file.name}: {str(e)}"}
