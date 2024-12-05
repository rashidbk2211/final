from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Facility, Department
from .forms import DoctorCreationForm, FacilityForm, DepartmentForm
from doctor.models import Doctor
from patient.models import Appointment

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    facilities = Facility.objects.all()
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    pending_appointments = Appointment.objects.filter(status='PENDING')
    return render(request, 'administrator/dashboard.html', {
        'users': users,
        'facilities': facilities,
        'departments': departments,
        'doctors': doctors,
        'pending_appointments': pending_appointments,
    })

@login_required
@user_passes_test(is_admin)
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully')
            return redirect('admin_dashboard')
    else:
        form = DoctorCreationForm()
    return render(request, 'administrator/add_doctor.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST, instance=doctor.user)
        if form.is_valid():
            form.save()
            doctor.specialization = form.cleaned_data['specialization']
            doctor.license_number = form.cleaned_data['license_number']
            doctor.qualification = form.cleaned_data['qualification']
            doctor.experience_years = form.cleaned_data['experience_years']
            doctor.consultation_fee = form.cleaned_data['consultation_fee']
            doctor.save()
            messages.success(request, 'Doctor updated successfully')
            return redirect('admin_dashboard')
    else:
        form = DoctorCreationForm(instance=doctor.user, initial={
            'specialization': doctor.specialization,
            'license_number': doctor.license_number,
            'qualification': doctor.qualification,
            'experience_years': doctor.experience_years,
            'consultation_fee': doctor.consultation_fee,
        })
    return render(request, 'administrator/edit_doctor.html', {'form': form, 'doctor': doctor})

@login_required
@user_passes_test(is_admin)
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'CONFIRMED'
    appointment.save()
    messages.success(request, 'Appointment confirmed successfully')
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'REJECTED'
    appointment.save()
    messages.success(request, 'Appointment rejected')
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def manage_facility(request, facility_id=None):
    if facility_id:
        facility = get_object_or_404(Facility, id=facility_id)
    else:
        facility = None

    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, 'Facility saved successfully')
            return redirect('admin_dashboard')
    else:
        form = FacilityForm(instance=facility)

    return render(request, 'administrator/manage_facility.html', {'form': form, 'facility': facility})

@login_required
@user_passes_test(is_admin)
def manage_department(request, department_id=None):
    if department_id:
        department = get_object_or_404(Department, id=department_id)
    else:
        department = None

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department saved successfully')
            return redirect('admin_dashboard')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'administrator/manage_department.html', {'form': form, 'department': department})

