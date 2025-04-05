from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.contrib.auth.models import User

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
    
#ratings

# class Rating(models.Model):
    # RATING_CHOICES = [
    #     (1, '1 - Poor'),
    #     (2, '2 - Fair'),
    #     (3, '3 - Good'),
    #     (4, '4 - Very Good'),
    #     (5, '5 - Excellent')
    # ]
    
    # rated_user = models.ForeignKey(
    #     Profile,
    #     on_delete=models.CASCADE,
    #     related_name='ratings_received'
    # )
    # rating_user = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='ratings_given'
    # )
    # score = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(5)],
    #     choices=RATING_CHOICES
    # )
    # comment = models.TextField(blank=True)
    # service = models.ForeignKey(
    #     Service,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True
    # )
    # created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('rated_user', 'rating_user', 'service')
    #     ordering = ['-created_at']

    # def __str__(self):
    #     return f"{self.score} stars for {self.rated_user}"