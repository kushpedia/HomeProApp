from django.contrib import admin
from .models import Profile,LoginAttempt, Rating,Booking,BookingAttachment, TaskCompletion, ProofImage
# Register your models here.
admin.site.register(Profile)
admin.site.register(LoginAttempt)
admin.site.register(Rating)
admin.site.register(Booking)
admin.site.register(BookingAttachment)
admin.site.register(TaskCompletion)
admin.site.register(ProofImage)


