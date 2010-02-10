from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import CharField, DateTimeField, ModelForm

from sendinel.backend.models import HospitalAppointment


class HospitalAppointmentForm(ModelForm):
    date = DateTimeField(widget = AdminSplitDateTime())
    recipient = CharField(max_length = 255, label = "Patient name")
    class Meta:
        model = HospitalAppointment
        exclude = ['recipient_type', 'recipient_id']
        fields = ['recipient', 'date', 'hospital', 'doctor',
                    'way_of_communication']
        