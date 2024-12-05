from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from doctor.models import Doctor
from .models import Facility, Department


class DoctorCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    specialization = forms.CharField(max_length=255, required=True)
    license_number = forms.CharField(max_length=50, required=True)
    qualification = forms.CharField(max_length=255, required=True)
    experience_years = forms.IntegerField(min_value=0, required=True)
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                license_number=self.cleaned_data['license_number'],
                qualification=self.cleaned_data['qualification'],
                experience_years=self.cleaned_data['experience_years'],
                consultation_fee=self.cleaned_data['consultation_fee']
            )
        return user


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'address', 'phone_number']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'facility']

