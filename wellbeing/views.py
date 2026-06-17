from django.shortcuts import render
from .models import Employee
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        password = request.POST.get('password')

        try:
            Employee.objects.create(
                fullname=fullname,
                email=email,
                phone=phone,
                department=department,
                 password=make_password(password)
            )
            return render(request, 'register.html', {'msg': 'Registration Successful'})

        except IntegrityError:
            return render(request, 'register.html', {'msg': 'Email already exists!'})

    return render(request, 'register.html')

from django.shortcuts import render, redirect
from .models import Employee

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Employee.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.fullname
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = Employee.objects.get(id=request.session['user_id'])
    return render(request, 'dashboard.html', {'user': user})

def logout(request):
    request.session.flush()
    return redirect('login')