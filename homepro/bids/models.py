from django.db import models
from users.models import Profile, Booking
import uuid

# Create your models here.
class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'), 
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booking_bid_s'
    )
    provider = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='provider_bid_s'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['booking', 'provider'],
                name='unique_provider_bid_per_booking'
            )
        ]

    def __str__(self):
        return f"Bid for {self.booking.service.name},  Bidder:{self.provider.first_name},  Customer:{self.booking.user.first_name}"