from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=100)