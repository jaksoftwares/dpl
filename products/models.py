from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(verbose_name="Use case / Description")
    creation_date = models.DateField(default=timezone.now)
    version = models.CharField(max_length=50, blank=True, null=True)
    
    # Traceability fields
    project_ref = models.CharField(max_length=255, blank=True, null=True, help_text="Reference to the project that birthed this product")
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.name
