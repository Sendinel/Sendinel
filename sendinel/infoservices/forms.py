from django.forms import CharField, Form, ModelForm
from django.utils.translation import ugettext as _

from sendinel.infoservices.models import InfoService

class InfoMessageValidationForm(Form):
    text = CharField(error_messages={ \
                        'required': _('Please enter a text to send'), \
                        'invalid': _('The text contains invalid characters')})

class InfoServiceValidationForm(ModelForm):
    class Meta:
        model = InfoService
        exclude = ['members']

    name = CharField(error_messages={ \
                        'required': _('Please enter a name'), \
                        'invalid': _('The name contains invalid characters')})
