from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import make_aware
from users.models import Booking
from django.forms.widgets import FileInput

from django.utils.safestring import mark_safe


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['special_instructions']
        widgets = {
            'special_instructions': forms.Textarea(attrs={
                'class': 'your-css-classes',
                'rows': 3
            }),
        }
    
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[MinValueValidator(timezone.now().date())]
    )
    time_slot = forms.ChoiceField(
        choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')]
    )
    urgency = forms.ChoiceField(
        required=False,
        choices=[('normal', 'Normal'), ('urgent', 'Urgent (+20% fee)')]
    )
    

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('booking_date')
        time_slot = cleaned_data.get('time_slot')

        if not date or not time_slot:
            raise forms.ValidationError("Both date and time slot are required")

        # Convert to datetime
        start_hour = {
            'morning': 8,
            'afternoon': 12,
            'evening': 16
        }.get(time_slot, 8)

        try:
            booking_datetime = timezone.datetime.combine(
                date,
                timezone.datetime.min.time()
            ).replace(hour=start_hour)

            # Make the datetime timezone-aware
            booking_datetime = make_aware(booking_datetime)

            # # Validate booking time is at least 2 hours in the future
            # if booking_datetime <= timezone.now() + timedelta(hours=2):
            #     raise forms.ValidationError("Bookings require at least 2 hours advance notice")

            cleaned_data['date'] = booking_datetime

        except (TypeError, ValueError) as e:
            raise forms.ValidationError(f"Invalid date/time: {str(e)}")

        return cleaned_data