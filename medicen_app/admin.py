from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointments)
admin.site.register(Contact)
admin.site.register(Prescription)
