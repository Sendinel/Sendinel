from django.contrib import admin

from sendinel.backend.models import Patient, \
                                    Hospital, \
                                    ScheduledEvent, \
                                    AuthenticationCall, \
                                    WayOfCommunication
from sendinel.infoservices.models import InfoMessage, \
                                   InfoService, \
                                   Subscription, \
                                   InfoService
from sendinel.notifications.models import AppointmentType, \
                                          HospitalAppointment


admin.site.register(AppointmentType)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(HospitalAppointment)
admin.site.register(InfoMessage)
admin.site.register(InfoService)
admin.site.register(ScheduledEvent)
admin.site.register(AuthenticationCall)
admin.site.register(WayOfCommunication)
admin.site.register(Subscription)