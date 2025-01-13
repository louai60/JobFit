from PyPDF2 import PdfReader
import docx
import logging
import os
import subprocess
import tempfile
import pdfplumber  
import pdfminer  

logger = logging.getLogger(__name__)

def extract_text_pdf(file):
    """Extract text from a PDF file using PdfReader and pdfplumber for complex layouts."""
    try:
        file.seek(0)  # Ensure the file pointer is at the beginning
        reader = PdfReader(file)
        text = []

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
            else:
                logger.warning(f"Page {page_num + 1} did not contain extractable text.")
        
        extracted_text = "\n".join(text)

        # If no text extracted by PdfReader, try using pdfplumber (more reliable for complex PDFs)
        if not extracted_text:
            logger.info("Attempting to extract text using pdfplumber for complex layouts...")
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text()  # Extract with pdfplumber
                if not extracted_text:
                    raise ValueError("No text could be extracted from the PDF using both PyPDF2 and pdfplumber.")

        logger.debug(f"PDF Extraction - Pages: {len(reader.pages)}, Characters: {len(extracted_text)}")
        return extracted_text.strip()

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def extract_text_docx(file):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise

def extract_text_txt(file):
    """Extract text from a TXT file."""
    try:
        text = file.read().decode('utf-8')
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

        return result.stdout.strip()

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
