from django.db import models

class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.fullname

from django.db import models

class LoginActivity(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.employee.fullname