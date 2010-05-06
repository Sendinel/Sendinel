from django.forms import CharField, ChoiceField, DateTimeField, Textarea, \
                            Form, ModelForm
from django.utils.translation import ugettext as _

from sendinel.backend.authhelper import format_and_validate_phonenumber
from sendinel.backend.models import Sendable
from sendinel.groups.models import InfoMessage

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
    way_of_communication = ChoiceField(
                        choices = Sendable.WAYS_OF_COMMUNICATION,
                        error_messages={'required': \
                                _('Please choose a way of communication')})

class DateValidationForm(Form): 
    date = DateTimeField(error_messages={ \
                            'required': _('Please choose a date'), \
                            'invalid': _('Please choose a date')})                        
    


