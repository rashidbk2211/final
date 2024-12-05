from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.patient_registration, name='patient_registration'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('initiate-payment/<int:appointment_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/<int:appointment_id>/', views.payment_success, name='payment_success'),
    path('payment-cancel/<int:appointment_id>/', views.payment_cancel, name='payment_cancel'),
]

