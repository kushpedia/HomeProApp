from django import forms
from . models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'comment']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter your bid price'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }