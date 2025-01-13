from django.urls import path
from .views import list_jobs

urlpatterns = [
    path('', list_jobs, name='list_jobs'),
]