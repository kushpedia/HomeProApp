from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from services.models import Service
# Create your models here.
class  Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_image = models.FileField(null=True, blank=True, 
                                    upload_to='profiles/', default="profiles/user-default.png")
    location = models.CharField(max_length=200,null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=255) 
    bio = models.TextField(null=True, blank=True) 
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')
    
    # @property
    # def profileImageURL(self):
    #     try:
    #         url = self.profile_image.url
    #     except:
    #         url = ''
    #     return url
    
    
