from django.forms import CharField, ModelForm

from sendinel.backend.models import InfoMessage

class InfoMessageForm(ModelForm):
    
    text = CharField(max_length = 255, label = "Infoservice Text")
    
    class Meta:
        model = InfoMessage
        exclude = ['recipient']
        fields = ['text']
        