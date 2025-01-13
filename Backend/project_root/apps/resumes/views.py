from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db import transaction
from .models import Resume
from .serializers import ResumeSerializer
from .huggingface_parser import parse_resume_with_api   
from .pdf_extractor import extract_text_pdf, extract_text_docx, extract_text_txt, extract_text_rtf_odt
import logging
# from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def extract_text_from_resume(file):
    """
    Extracts text from different file formats (PDF, DOCX, TXT, etc.).
    """
    try:
        if file.name.endswith('.pdf'):
            return {'text': extract_text_pdf(file)}
        elif file.name.endswith('.docx'):
            return {'text': extract_text_docx(file)}
        elif file.name.endswith('.txt'):
            return {'text': extract_text_txt(file)}
        elif file.name.endswith('.rtf') or file.name.endswith('.odt'):
            return {'text': extract_text_rtf_odt(file)}
        else:
            return {'error': 'Unsupported file format. Please upload a PDF, DOCX, TXT, RTF, or ODT file.'}
    except Exception as e:
        logger.error(f"Failed to extract text from file {file.name}: {str(e)}")
        return {'error': f"Failed to extract text from file {file.name}: {str(e)}"}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # Ensure JWT token is used
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
                extracted_data = extract_text_from_resume(file)

                if "error" in extracted_data:
                    raise ValueError(extracted_data["error"])

                resume_text = extracted_data["text"]

                # Parse the extracted text
                logger.info("Parsing the extracted resume text.")
                parsed_data = parse_resume_with_api(resume_text)

                if "error" in parsed_data:
                    raise ValueError(parsed_data["error"])

                # Save the parsed data back to the resume
                resume.parsed_data = {"parsed_data": parsed_data}
                resume.save()

                logger.info(f"Resume processed successfully for user {request.user.id}")
                return Response({
                    "message": "Resume processed successfully",
                    "data": ResumeSerializer(resume).data
                }, status=200)

            return Response(serializer.errors, status=400)

    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        return Response({
            "error": f"An error occurred while processing the resume: {str(e)}"
        }, status=500)


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
    try:
        # Ensuring parsed_data is a list and contains dictionaries
        if not isinstance(parsed_data, list) or not all(isinstance(item, dict) for item in parsed_data):
            raise ValueError("Parsed data is not in the expected format: List of dictionaries required.")

        # Processing each entity in the parsed data
        for entity in parsed_data:
            entity_group = entity.get('entity_group')
            if entity_group == 'SKILL':
                resume.skills.append(entity['word'])
            elif entity_group == 'EXPERIENCE':
                resume.experience.append(entity['word'])
            elif entity_group == 'EDUCATION':
                resume.education.append(entity['word'])

        resume.save()
    except Exception as e:
        logger.error(f"Error updating resume with parsed data: {str(e)}")
        raise
