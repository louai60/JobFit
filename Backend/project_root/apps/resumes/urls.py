from django.urls import path
from .views import upload_and_process_resume, get_resume_details

urlpatterns = [
    path('upload/', upload_and_process_resume, name='upload_resume'),
    path('<int:resume_id>/', get_resume_details, name='get_resume_details'),
]