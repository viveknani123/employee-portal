from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import Employee, LoginActivity
from django.db.models import Q
from django.http import HttpResponse
import csv
from django.db.models import Count
import json



# Home Page
def home(request):
    return render(request, 'index.html')


# Register Page
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

            return render(
                request,
                'register.html',
                {'msg': 'Registration Successful'}
            )

        except IntegrityError:
            return render(
                request,
                'register.html',
                {'msg': 'Email already exists!'}
            )

    return render(request, 'register.html')


# Login Page
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Get user by email
        user = Employee.objects.filter(email=email).first()
        print("User found:", user)
        # Check hashed password
        if user and check_password(password, user.password):
            # Save login activity
            LoginActivity.objects.create(
                employee=user,
                status='Logged In'
            )

            # Create session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.fullname
            request.session['is_admin'] = user.is_admin

            return redirect('dashboard')

        # Invalid credentials
        return render(
            request,
            'login.html',
            {'error': 'Invalid Email or Password'}
        )

    return render(request, 'login.html')


# Dashboard
def dashboard(request):

    if 'user_id' not in request.session:
        return redirect('login')

    total_employees = Employee.objects.count()
    total_departments = Employee.objects.values(
        'department'
    ).distinct().count()
    total_logins = LoginActivity.objects.count()
    department_data = (
        Employee.objects
        .values('department')
        .annotate(count=Count('id'))
    )

    labels = [item['department'] for item in department_data]
    counts = [item['count'] for item in department_data]

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_logins': total_logins,
        'labels': json.dumps(labels),
        'counts': json.dumps(counts),
    }

    return render(
        request,
        'dashboard.html',
        context
    )
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('dashboard')

    if 'user_id' not in request.session:
        return redirect('login')

    total_employees = Employee.objects.count()
    total_logins = LoginActivity.objects.count()
    departments = Employee.objects.values(
        'department'
    ).distinct().count()

    context = {
        'total_employees': total_employees,
        'total_logins': total_logins,
        'departments': departments,
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )
def employees(request):

    search = request.GET.get('search')

    if search:
        employees = Employee.objects.filter(
            Q(fullname__icontains=search) |
            Q(email__icontains=search) |
            Q(department__icontains=search)
        )
    else:
        employees = Employee.objects.all()

    context = {
        'employees': employees
    }

    return render(
        request,
        'employees.html',
        context
    )
def add_employee(request):

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

            return redirect('employees')

        except IntegrityError:
            return render(
                request,
                'add_employee.html',
                {'msg': 'Email already exists!'}
            )

    return render(request, 'add_employee.html')

def edit_employee(request, id):

    employee = Employee.objects.get(id=id)

    if request.method == 'POST':

        employee.fullname = request.POST.get('fullname')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.department = request.POST.get('department')

        employee.save()

        return redirect('employees')

    context = {
        'employee': employee
    }

    return render(
        request,
        'edit_employee.html',
        context
    )
    
def view_employee(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'view_employee.html', {'employee': employee})


def edit_employee(request, id):
    if not request.session.get('is_admin'):
     return redirect('dashboard')
    employee = Employee.objects.get(id=id)

    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.email = request.POST['email']
        employee.department = request.POST['department']
        employee.salary = request.POST['salary']
        employee.save()
        return redirect('home')

    return render(request, 'edit_employee.html', {'employee': employee})
def delete_employee(request, id):
    if not request.session.get('is_admin'):
        return redirect('dashboard')
    Employee.objects.filter(id=id).delete()

    return redirect('employees')

def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'ID',
        'Full Name',
        'Email',
        'Phone',
        'Department'
    ])

    employees = Employee.objects.all()

    for e in employees:
        writer.writerow([
            e.id,
            e.fullname,
            e.email,
            e.phone,
            e.department
        ])

    return response


# Logout
def logout(request):
    request.session.flush()
    return redirect('login')