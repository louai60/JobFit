from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.db import transaction
from .models import Resume
from .serializers import ResumeSerializer
from .spacy.spacy_parser import parse_resume
from .pdf_extractor import (extract_text_pdf, extract_text_docx, extract_text_txt, extract_text_rtf_odt)
import logging

logger = logging.getLogger(__name__)

def extract_text_from_resume(file):
    """
    Extracts text from different file formats (PDF, DOCX, TXT, etc.).
    """
    try:
        if file.name.endswith('.pdf'):
            text = extract_text_pdf(file)
        elif file.name.endswith('.docx'):
            text = extract_text_docx(file)
        elif file.name.endswith('.txt'):
            text = extract_text_txt(file)
        elif file.name.endswith('.rtf') or file.name.endswith('.odt'):
            text = extract_text_rtf_odt(file)
        else:
            raise ValueError("Unsupported file format. Please upload a PDF, DOCX, TXT, RTF, or ODT file.")

        # Ensure the extracted text is a string
        if not isinstance(text, str):
            text = str(text)

        return text
    except Exception as e:
        logger.error(f"Failed to extract text from file {file.name}: {str(e)}")
        raise

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def upload_and_process_resume(request):
    """
    Handles the upload and parsing of a resume.
    """
    try:
        with transaction.atomic():
            # Deactivate previous resumes for the user
            Resume.objects.filter(user=request.user, is_active=True).update(is_active=False)

            # Validate and save the uploaded resume
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                resume = serializer.save(user=request.user)

                # Extract text from the uploaded file
                file = resume.file
                logger.info(f"Extracting text from file: {file.name}")
                try:
                    text = extract_text_from_resume(file)
                except ValueError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Log the extracted text for debugging
                logger.info(f"Extracted text: {text[:100]}...")  # Log first 100 chars

                # Parse the extracted text using spaCy
                logger.info("Parsing the extracted resume text with spaCy.")
                parsed_data = parse_resume(text)

                # Log the parsed data for debugging
                logger.info(f"Parsed data: {parsed_data}")

                # Ensure parsed_data has the required keys
                parsed_data.setdefault("skills", [])
                parsed_data.setdefault("experience", [])
                parsed_data.setdefault("education", [])

                # Update resume with parsed data
                update_resume_with_parsed_data(resume, parsed_data)

                logger.info(f"Resume processed successfully for user {request.user.id}")
                return Response({
                    "message": "Resume processed successfully",
                    "data": ResumeSerializer(resume).data
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}", exc_info=True)  # Log full traceback
        return Response({
            "error": f"An error occurred while processing the resume: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resume_details(request, resume_id):
    """
    Retrieves the details of a specific resume.
    """
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Resume.DoesNotExist:
        logger.error(f"Resume with ID {resume_id} not found for user {request.user.id}")
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

def update_resume_with_parsed_data(resume, parsed_data):
    """
    Updates the resume model with parsed data from spaCy.
    """
    try:
        # Update the parsed_data field
        resume.parsed_data = parsed_data
        resume.save()
    except Exception as e:
        logger.error(f"Error updating resume with parsed data: {str(e)}")
        raise