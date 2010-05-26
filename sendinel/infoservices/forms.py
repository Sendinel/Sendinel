from django.forms import CharField, Form
from django.utils.translation import ugettext as _


class InfoMessageValidationForm(Form):
    text = CharField(error_messages={ \
                        'required': _('Please enter a text to send'), \
                        'invalid': _('The text contains invalid characters')})

class InfoserviceValidationForm(Form): 
    name = CharField(error_messages={ \
                        'required': _('Please enter a name'), \
                        'invalid': _('The name contains invalid characters')})
