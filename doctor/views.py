from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Doctor
from patient.models import Appointment, Patient

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'doctor')

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date_time')
    return render(request, 'doctor/dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
    })

@login_required
@user_passes_test(is_doctor)
def patient_details(request, patient_id):
    doctor = request.user.doctor
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(doctor=doctor, patient=patient).order_by('-date_time')
    return render(request, 'doctor/patient_details.html', {
        'patient': patient,
        'appointments': appointments,
    })

