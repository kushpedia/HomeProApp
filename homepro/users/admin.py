from django.contrib import admin
from .models import Profile,LoginAttempt, Rating,Booking,BookingAttachment
# Register your models here.
admin.site.register(Profile)
admin.site.register(LoginAttempt)
admin.site.register(Rating)
admin.site.register(Booking)
admin.site.register(BookingAttachment)

