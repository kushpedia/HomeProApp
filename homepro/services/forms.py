from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from django.forms.widgets import ClearableFileInput
from users.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['special_instructions', 'attachments']
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
    attachments = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': False,
                                            'class': 'your-upload-class',
                                            'accept': 'image/*'
                                            })
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
        }.get(time_slot, 8)  # Default to morning if invalid
        
        try:
            booking_datetime = timezone.datetime.combine(
                date, 
                timezone.datetime.min.time()
            ).replace(hour=start_hour)
            cleaned_data['date'] = booking_datetime
        except (TypeError, ValueError) as e:
            raise forms.ValidationError(f"Invalid date/time: {str(e)}")
            
        return cleaned_data