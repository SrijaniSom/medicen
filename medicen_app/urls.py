from django.conf.urls.static import static
from medicen_prj.settings import MEDIA_ROOT
from os import name
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name ='index'),
    path('signup', signupuser, name='signupuser'),
    path('login', loginuser, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
    path('logindoctor',logindoctor,name="logindoctor"),
    path('signupdoctor',signupdoctor,name="signupdoctor"),
    path("appointment/<int:id>",appointment,name="appointment"),
    path("appointment_request/<int:id>",appointment_request,name="appointment_request"),
    path('todo/<int:todo_pk>/complete', completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', deletetodo, name='deletetodo'),
    path("upcoming_appointments/<int:id>",upcoming_list,name="upcoming_appointments"),
    path("view_prescribe/<int:id>",view_prescibe,name="view_prescribe"),
    path("prescribe_update/<int:id>",prescribe_update,name="prescribe_update"),
    path("patient_reports/<int:id>",patient_reports,name="patient_reports"),
    path("report_details/<int:id>",report_details,name="report_details"),
    path("contact",contact,name="contact"),
    path("services",services,name="services"),
    path("doctors",doctors,name="doctors"),
    path("doctor-admin",doctor_admin,name="doctor_admin"),
    path("previous_list/<int:id>",previous_list,name="previous_list"),
    path("doctor_index",doctor_index,name="doctor_index"),
    path("patient-admin",patient_admin,name="patient_admin"),
    path("patient_index",patient_index,name="patient_index"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)