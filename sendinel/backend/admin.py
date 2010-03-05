from django.contrib import admin

from sendinel.backend.models import *

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(HospitalAppointment)
admin.site.register(InfoMessage)
admin.site.register(ScheduledEvent)
admin.site.register(AuthenticationCall)
