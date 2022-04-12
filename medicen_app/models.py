from secrets import choice
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(null=None, max_length=50)
    desc = models.CharField(null=None,max_length=100, default="Department")
    img = models.CharField(null=None,max_length=500,default="Department")
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    doctorid = models.CharField(null=True,max_length=200)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    qualification = models.CharField(null=None, max_length=50)
    img = models.CharField(null=None,max_length=500,default="Department")
    email = models.EmailField()
    phone = models.BigIntegerField()
    

    def __str__(self):
        return self.doctor.username

class Patient(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    email = models.EmailField()
    phone = models.BigIntegerField()
    
    def __str__(self):
        return self.patient.username

class Appointments(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    accepted = models.BooleanField()
    checked = models.BooleanField()

    def __str__(self):
        return (f'{self.doctor},{self.patient},{self.date}')

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    subject = models.CharField(max_length=500)
    message = models.TextField()

    def __str__(self):
        return self.name


class Prescription(models.Model):
    term = ( ('longterm','longterm'),
    ('shortterm','shortterm'))
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE,null=True)
    desc = models.TextField()
    prescribe = models.TextField()
    tests = models.TextField()
    report = models.FileField()
    term = models.CharField(choices=term,max_length=200,default="shortterm")
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return (f'{self.appointment.patient} treated by {self.appointment.doctor}')


