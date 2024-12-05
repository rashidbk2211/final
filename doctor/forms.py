from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medications', 'instructions']
        widgets = {
            'medications': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
        }

