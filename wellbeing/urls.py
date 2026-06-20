from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path(
    'employees/',
    views.employees,
    name='employees'
),
path(
    'edit/<int:id>/',
    views.edit_employee,
    name='edit_employee'
),

path(
    'view/<int:id>/',
    views.view_employee,
    name='view_employee'
),

path(
    'delete/<int:id>/',
    views.delete_employee,
    name='delete_employee'
),

path(
    'export-csv/',
    views.export_csv,
    name='export_csv'
),
path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
]