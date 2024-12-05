from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name} - {self.facility}"

class AdministratorProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='administrator_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Administrator: {self.user.get_full_name()} ({self.employee_id})"

