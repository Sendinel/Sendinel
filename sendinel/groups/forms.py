from django.forms import CharField, DateTimeField, Textarea, \
                            Form, ModelForm, ModelChoiceField
from django.utils.translation import ugettext as _

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import get_enabled_wocs, \
                                    get_immediate_wocs
from sendinel.infoservices.models import InfoMessage, InfoService

class InfoMessageForm(ModelForm):
    
    text = CharField(max_length = 160, 
                    label = "Infoservice Text",
                    widget=Textarea(attrs={
                        'rows': '5',
                        'cols': '35'})
                    ) 
    
    class Meta:
        model = InfoMessage
        exclude = ['recipient']
        fields = ['text']

class InfoserviceValidationForm(Form): 
    name = CharField(error_messages={ \
                        'required': _('Please enter a name'), \
                        'invalid': _('The name contains invalid characters')})
                            
class InfoMessageValidationForm(Form):
    text = CharField(error_messages={ \
                        'required': _('Please enter a text to send'), \
                        'invalid': _('The text contains invalid characters')})

class NotificationValidationForm2(Form):
    phone_number = CharField(validators = [format_and_validate_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
    way_of_communication = ModelChoiceField(
                        queryset = get_immediate_wocs(),
                        error_messages={'required': \
                                _('Please choose a way of communication')})

class RegisterPatientForMedicineForm(Form):  
    phone_number = CharField(validators = [format_and_validate_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
    way_of_communication = ModelChoiceField(
                        queryset = get_enabled_wocs(),
                        error_messages={'required': \
                                _('Please choose a way of communication')})     
    medicine = ModelChoiceField(
            queryset=InfoService.objects.all().filter(type='medicine'),
            error_messages={'required': \
                            _('Please choose a medicine')})

class RegisterPatientForNewMedicineForm(Form):  
    phone_number = CharField(validators = [format_and_validate_phonenumber],
            error_messages={'required':_('Please enter a phone number')})
    way_of_communication = ModelChoiceField(
                        queryset = get_enabled_wocs(),
                        error_messages={'required': \
                                _('Please choose a way of communication')}) 
                            
class DateValidationForm(Form): 
    date = DateTimeField(error_messages={ \
                            'required': _('Please choose a date'), \
                            'invalid': _('Please choose a date')})   

class MedicineMessageValidationForm(Form):
    medicine = ModelChoiceField(
                queryset=InfoService.objects.all().filter(type='medicine'),
                error_messages={'required': \
                                _('Please choose a medicine'), \
                                'invalid_choice':  \
                                _('Please choose a medicine')})                            
    text = CharField(error_messages={ \
                        'required': _('Please enter a text to send'), \
                        'invalid': _('The text contains invalid characters')})