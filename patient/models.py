from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.username}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ], default='PENDING')

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date_time}"

    def save(self, *args, **kwargs):
        if self.payment_status == 'PAID' and self.status == 'PENDING':
            self.status = 'PENDING'  # Keep it pending even if paid, waiting for admin confirmation
        super().save(*args, **kwargs)

