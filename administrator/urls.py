from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('confirm-appointment/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('reject-appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
]

