from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from users.models import Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'special_instructions']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_instructions': forms.Textarea(attrs={'rows': 3,'class':'mb-4 bg-white border border-[var(--accent-blue)]/30 text-[var(--navy-blue)] text-sm rounded-lg focus:ring-[var(--accent-blue)] focus:border-[var(--accent-blue)] block w-full p-2.5','placeholder':'Describe Your Task,Give all the details'})
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now() + timedelta(hours=2):
            raise ValidationError("Booking must be at least 2 hours from now")
        return date