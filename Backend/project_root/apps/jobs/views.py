from django.http import JsonResponse
from .models import Job

def list_jobs(request):
    jobs = Job.objects.all()
    job_data = [{'id': job.id, 'title': job.title, 'description': job.description} for job in jobs]
    return JsonResponse(job_data, safe=False)