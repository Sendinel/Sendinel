from django.forms import CharField, DateTimeField, Form, ModelChoiceField
from django.utils.translation import ugettext as _

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import get_immediate_wocs
from sendinel.infoservices.models import InfoMessage, InfoService


class RegisterPatientForGroupValidationForm(Form):
    phone_number = CharField(validators = [format_and_validate_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
    way_of_communication = ModelChoiceField(
                        queryset = get_immediate_wocs(),
                        error_messages={'required': \
                                _('Please choose a way of communication')})
