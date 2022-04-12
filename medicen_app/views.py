from pydoc import doc
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def signupdoctor(request):
    dept = Department.objects.all()
    if request.method == 'GET':
        return render(request, 'doctor/register-hacks.html', {'form':UserCreationForm(),'dept':dept})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                depart = request.POST['dept']
                de = Department.objects.get(id=depart)
                user = User.objects.create(request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
                user.save()
                doctor = Doctor.objects.create(doctor=user,dept=de,qualification=request.POST['qualification'],phone=request.POST['phone'],email=request.POST['email'],doctorid=request.POST['docid'])
                doctor.save()
                login(request, user)
                return redirect('doctor_index')
            except IntegrityError:
                return render(request, 'doctor/register-hacks.html', {'form':UserCreationForm(), 'error':'That username or email has already been taken !','dept':dept})
        else:
            return render(request, 'doctor/register-hacks.html', {'form':UserCreationForm(), 'error':'Passwords did not match','dept':dept})

def logindoctor(request):
    if request.method == 'GET':
        return render(request, 'doctor/login-hacks.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'doctor/login-hacks.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('doctor_index')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'patient/register-hack.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create(username=request.POST['username'], password=request.POST['password1'],email=request.POST['email'])
                user.save()
                patient = Patient.objects.create(patient=user,email=request.POST['email'],phone=request.POST['phone'])
                patient.save()
                login(request, user)
                return redirect('patient_index')
            except IntegrityError:
                return render(request, 'patient/register-hack.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'patient/register-hack.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'patient/login-hack.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print("no user")
            return render(request, 'patient/login-hack.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('patient_index')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('index')

def appointment(request,id):
    doctors = Doctor.objects.all()
    user = User.objects.get(id=id)
    patient = Patient.objects.get(patient=user)
    if request.method == "POST":
        doctor = request.POST['doctor']
        date = request.POST['date']
        doctor = Doctor.objects.get(id=doctor)
        app = Appointments.objects.create(patient=patient,doctor=doctor,date=date,accepted=False,checked=False)
        app.save()
        messages.success(request,"Appointent done !")
        return redirect('patient_admin')
    else:
        return render(request,"appointment-booking.html",{'doctors':doctors})


def appointment_request(request,id):
    user = User.objects.get(id=id)
    doctor = Doctor.objects.get(doctor=user)
    appointments = Appointments.objects.filter(doctor=doctor,accepted=False)
    return render(request,"doctor/acceptdecline.html",{'appointments':appointments})


def completetodo(request, todo_pk):
    todo = get_object_or_404(Appointments, pk=todo_pk)
    if request.method == 'POST':
        todo.accepted = True
        todo.save()
        messages.error(request,"Appointment acccepted !!")
        return redirect('index')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Appointments, pk=todo_pk)
    if request.method == 'POST':
        todo.delete()
        messages.error(request,"appointment deleted !!")
        return redirect('index')

def contact(request):
    if request.method == "POST":
        contact = Contact.objects.create(name=request.POST['name'],phone=request.POST['phone'],email=request.POST['email'],subject=request.POST['subject'],message=request.POST['message'])
        contact.save()
        return redirect('index')

def upcoming_list(request,id):
    user = User.objects.get(id=id)
    doctor = Doctor.objects.get(doctor=user)
    appointments = Appointments.objects.filter(doctor=doctor,accepted=True,checked=False)
    return render(request,"doctor/appointmentsTable.html",{'appointments':appointments})

def previous_list(request,id):
    user = User.objects.get(id=id)
    doctor = Doctor.objects.get(doctor=user)
    appointments = Appointments.objects.filter(doctor=doctor,accepted=True,checked=True)
    return render(request,"doctor/previous.html",{'appointments':appointments})

def view_prescibe(request,id):
    app = Appointments.objects.get(id=id)
    if Prescription.objects.filter(appointment=app).exists():
        pre = Prescription.objects.get(appointment=app)
    else:
        pre = {}
    return render(request,'doctor/record-view.html',{'pre':pre,'app':app})

def prescribe_update(request,id):
    app = Appointments.objects.get(id=id)
    if request.method == "POST":
        desc = request.POST['desc']
        prescibe = request.POST['prescribe']
        tests = request.POST['tests']
        upload = request.FILES["reports"]
        term = request.POST.get('term')
        if Prescription.objects.filter(appointment=app).exists():
            pre = Prescription.objects.filter(appointment=app)
            if upload is not None:
                pre.update(desc=desc,prescribe=prescibe,tests=tests,report=upload)
            else:
                pre.update(desc=desc,prescribe=prescibe,tests=tests)
        else:
            pre = Prescription.objects.create(appointment=app,desc=desc,prescribe=prescibe,tests=tests,report=upload)
            pre.save()
        if term == "longterm":
            pre = Prescription.objects.get(appointment=app)
            pre.term = "longterm"
            pre.save()
        else:
            pre = Prescription.objects.get(appointment=app)
            pre.term = "shortterm"
            pre.save()
        app.checked = True
        app.save()
        return redirect('index')
    else:
        if Prescription.objects.filter(appointment=app).exists():
            pre = Prescription.objects.get(appointment=app)
        else:
            pre = {}
        return render(request,'doctor/record-update.html',{'app':app,'pre':pre})

def patient_reports(request,id):
    user = User.objects.get(id=id)
    patient = Patient.objects.get(patient=user)
    app = Appointments.objects.filter(patient=patient)
    return render(request,"patient/patientrec.html",{'app':app})

def report_details(request,id):
    app = Appointments.objects.get(id=id)
    if Prescription.objects.filter(appointment=app).exists():
        pre = Prescription.objects.get(appointment=app)
    else:
        pre = {}
    return render(request,"patient/report_detail.html",{'app':app,'pre':pre})

def contact(request):
    if request.method == "POST":
        con = Contact.objects.create(name=request.POST['name'],email=request.POST['email'],phone=request.POST['phone'],subject=request.POST['subject'],message=request.POST['message'])
        con.save()
        return redirect('index')

def services(request):
    dept = Department.objects.all()
    return render(request,"services.html",{'dept':dept})

def doctors(request):
    doc = Doctor.objects.all()
    return render(request,'doctor.html',{'doc':doc})

def doctor_admin(request):
    if Doctor.objects.filter(doctor=request.user).exists():
        doc = Doctor.objects.get(doctor=request.user)
    else:
        doc = {}
    return render(request,"doctor/doctor-admin.html",{'doc':doc})

def patient_admin(request):
    if Patient.objects.filter(patient=request.user).exists():
        doc = Patient.objects.get(patient=request.user)
    else:
        doc = {}
    return render(request,"patient/patient-admin.html",{'doc':doc})

def doctor_index(request):
    if Doctor.objects.filter(doctor=request.user).exists():
        doc = Doctor.objects.get(doctor=request.user)
    else:
        doc = {}
    return render(request,"doctor/doc_index.html",{'doc':doc})

def patient_index(request):
    if Patient.objects.filter(patient=request.user).exists():
        doc = Patient.objects.get(patient=request.user)
    else:
        doc = {}
    return render(request,"patient/patient_index.html",{'doc':doc})
