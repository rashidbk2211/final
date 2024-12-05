from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Patient, Appointment
from .forms import PatientRegistrationForm, AppointmentForm
import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to E-Hospitality!')
            return redirect('patient_dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'patient/registration.html', {'form': form})


@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'patient/dashboard.html', {'appointments': appointments})


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('initiate_payment', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'patient/book_appointment.html', {'form': form})


@login_required
def initiate_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)

    if request.method == 'POST':
        try:
            intent = stripe.PaymentIntent.create(
                amount=1000,  # Amount in cents (e.g., $10.00)
                currency='usd',
                metadata={'appointment_id': appointment.id}
            )
            return JsonResponse({
                'clientSecret': intent.client_secret
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

    context = {
        'appointment': appointment,
        'stripe_publishable_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'patient/payment.html', context)


@login_required
def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    appointment.payment_status = 'PAID'
    appointment.save()
    messages.success(request, 'Payment successful. Your appointment is pending administrator confirmation.')
    return render(request, 'patient/payment_success.html', {'appointment': appointment})


@login_required
def payment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    appointment.delete()
    return render(request, 'patient/payment_cancel.html')


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    if appointment.status == 'PENDING' or appointment.status == 'CONFIRMED':
        appointment.status = 'CANCELLED'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully')
    else:
        messages.error(request, 'Cannot cancel this appointment')
    return redirect('patient_dashboard')

