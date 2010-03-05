from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import CharField, DateTimeField, ModelForm

from sendinel.backend.models import HospitalAppointment


class HospitalAppointmentForm(ModelForm):
    date = DateTimeField(widget = AdminSplitDateTime())
    recipient_name = CharField(max_length = 255, label = "Patient name")
    
    class Meta:
        model = HospitalAppointment
        exclude = ['recipient_type', 'recipient_id', 'hospital']
        fields = ['recipient_name', 'date', 'doctor',
                    'way_of_communication']
        