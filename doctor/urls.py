from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/<int:patient_id>/', views.patient_details, name='patient_details'),
]

