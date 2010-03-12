from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import CharField, DateTimeField, ModelForm

from sendinel.backend.models import HospitalAppointment


class HospitalAppointmentForm(ModelForm):
    date = DateTimeField(widget = AdminSplitDateTime())
    
    class Meta:
        model = HospitalAppointment
        exclude = ['recipient_type', 'recipient_id', 'hospital']
        fields = ['date', 'doctor', 'way_of_communication']
        