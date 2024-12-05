from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50)
    qualification = models.CharField(max_length=255)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"

    def get_full_name(self):
        return f"Dr. {self.user.get_full_name()}"

