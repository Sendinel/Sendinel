from django.forms import CharField, ChoiceField, DateTimeField, Form
from sendinel.backend.models import Sendable
from sendinel.backend.authhelper import format_phonenumber

class NotificationValidationForm(Form):
    recipient = CharField(validators = [format_phonenumber])
    date = DateTimeField()
    way_of_communication = ChoiceField(
                        choices = Sendable.WAYS_OF_COMMUNICATION)
                        
    



