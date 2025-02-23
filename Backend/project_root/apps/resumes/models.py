from django.db import models
from django.utils import timezone
from apps.users.models import CustomUser

class Resume(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    parsed_data = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(default=timezone.now)  # Add default value
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Resume for {self.user.username}"