from django.forms import CharField, Form, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import get_enabled_wocs
from sendinel.infoservices.models import InfoMessage, InfoService


class RegisterPatientForMedicineForm(Form):  
    phone_number = CharField(validators = [format_and_validate_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
    way_of_communication = ModelChoiceField(
                        queryset = get_enabled_wocs(),
                        error_messages={'required': \
                                _('Please choose a way of communication')})     
    medicine = ModelChoiceField(
            queryset=InfoService.objects.filter(type='medicine'),
            error_messages={'required': \
                                _('Please choose a medicine'),
                            'invalid_choice':
                                _('Please choose a medicine')})

class MedicineMessageValidationForm(Form):
    medicine = ModelChoiceField(
                queryset=InfoService.objects.filter(type='medicine'),
                error_messages={'required': \
                                _('Please choose a medicine'), \
                                'invalid_choice':  \
                                _('Please choose a medicine')})                            
    text = CharField(error_messages={ \
                        'required': _('Please enter a text to send'), \
                        'invalid': _('The text contains invalid characters')})
