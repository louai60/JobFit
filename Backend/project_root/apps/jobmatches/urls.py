from django.urls import path
from .views import list_job_matches

urlpatterns = [
    path('', list_job_matches, name='list_job_matches'),
]