from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            elif hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid user type')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

