from django.contrib import admin

from sendinel.backend.models import *

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(HospitalAppointment)
admin.site.register(InfoService)
admin.site.register(ScheduledEvent)

