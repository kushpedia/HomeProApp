from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from services.models import Service
# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
    ('customer', 'Customer'),
    ('provider', 'Service Provider'),
    ('both', 'Both'),
    ]
    PAYMENT_CHOICES = [
    ('mpesa', 'Mpesa'),
    ('Paypal', 'Paypal'),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255,null=True)
    profile_image = models.FileField(null=True, blank=True, 
                                    upload_to='profiles/', default="profiles/user-default.png")
    bio = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255)         
        # Role to differentiate users
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    # Customer fields
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255,blank=True, null=True)
    location_latitude = models.FloatField(blank=True, null=True)
    location_longitude = models.FloatField(blank=True, null=True)
    preferred_payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='mpesa')
    preferred_services = models.JSONField(blank=True, null=True)
    booking_history = models.JSONField(blank=True, null=True)

    # Service Provider fields
    services = models.ManyToManyField(Service, blank=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    certifications = models.JSONField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    reviews = models.JSONField(blank=True, null=True)
    availability_status = models.BooleanField(default=False)
    background_check_status = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    total_completed_tasks = models.IntegerField(default=0)
    badges_earned = models.JSONField(blank=True, null=True)
    subscription_plan = models.CharField(max_length=50, blank=True, null=True)

        # Verification and timestamps
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return f"{self.full_name} Role: {self.role}"
# login attempts

class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loginattempt')
    attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)
    last_attempt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.attempts} attempts"