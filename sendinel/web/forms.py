from django.forms import CharField, ChoiceField, DateTimeField, Form
from django.utils.translation import ugettext as _

from sendinel.backend.models import Sendable
from sendinel.backend.authhelper import format_phonenumber


class NotificationValidationForm(Form):
    recipient = CharField(validators = [format_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
                
    date = DateTimeField(error_messages={ \
                            'required': _('Please choose a date'), \
                            'invalid': _('Please choose a date')})
    way_of_communication = ChoiceField(
                        choices = Sendable.WAYS_OF_COMMUNICATION,
                        error_messages={'required': \
                                _('Please choose a way of communication')}) 
                        
    



