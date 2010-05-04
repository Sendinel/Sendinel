from django.forms import CharField, ModelForm, Textarea, Form
from django.utils.translation import ugettext as _

from sendinel.backend.models import InfoMessage

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