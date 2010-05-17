from django.forms import CharField, ModelChoiceField, DateTimeField, Form
from django.utils.translation import ugettext as _

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import Sendable, WayOfCommunication


class NotificationValidationForm(Form):
    phone_number = CharField(validators = [format_and_validate_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
        
    way_of_communication = ModelChoiceField(
                        queryset = WayOfCommunication.get_enabled_wocs(),
                        error_messages={'required': \
                                _('Please choose a way of communication')})
    date = DateTimeField(error_messages={ \
                            'required': _('Please choose a date'), \
                            'invalid': _('Please choose a date')})                                 

