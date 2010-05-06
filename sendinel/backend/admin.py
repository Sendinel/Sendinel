from django.contrib import admin

from sendinel.backend.models import AppointmentType, Patient, Hospital, \
                                    HospitalAppointment, \
                                    InfoMessage, \
                                    InfoService, \
                                    ScheduledEvent, \
                                    AuthenticationCall, \
                                    Subscription, \
                                    InfoService

admin.site.register(AppointmentType)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(HospitalAppointment)
admin.site.register(InfoMessage)
admin.site.register(InfoService)
admin.site.register(ScheduledEvent)
admin.site.register(AuthenticationCall)
admin.site.register(Subscription)
