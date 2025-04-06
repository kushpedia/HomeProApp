from django.db import models

import uuid


# Create your models here.
class ServiceCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    icon = models.FileField(null=True, blank=True, 
                                    upload_to='categories/', default="categories/user-default.png")
    description = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "ServiceCategory"
        verbose_name_plural = "Categories"


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    description = models.TextField(null=True, blank=True) 
    icon = models.FileField(null=True, blank=True, 
                                    upload_to='services/', default="services/user-default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    # Bookings

