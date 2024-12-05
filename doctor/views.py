from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Doctor, Prescription
from patient.models import Appointment, Patient
from .forms import PrescriptionForm
from django.contrib import messages


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
    prescriptions = Prescription.objects.filter(doctor=doctor, patient=patient).order_by('-date')
    return render(request, 'doctor/patient_details.html', {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
    })


@login_required
@user_passes_test(is_doctor)
def add_prescription(request, patient_id):
    doctor = request.user.doctor
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = doctor
            prescription.patient = patient
            prescription.save()
            messages.success(request, 'Prescription added successfully.')
            return redirect('patient_details', patient_id=patient_id)
    else:
        form = PrescriptionForm()

    return render(request, 'doctor/add_prescription.html', {
        'form': form,
        'patient': patient,
    })

