from django.db import models
from apps.users.models import CustomUser

class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    parsed_data = models.JSONField(default=list)  
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
