from django.http import JsonResponse
from .models import JobMatch
from django.contrib.auth.decorators import login_required

@login_required
def list_job_matches(request):
    matches = JobMatch.objects.filter(resume__user=request.user)
    match_data = [{'job_id': match.job.id, 'match_percentage': match.match_percentage} for match in matches]
    return JsonResponse(match_data, safe=False)