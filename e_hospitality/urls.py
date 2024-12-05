from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import custom_login

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('administrator/', include('administrator.urls')),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

