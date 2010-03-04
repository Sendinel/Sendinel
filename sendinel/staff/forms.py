from django.forms import CharField, DateTimeField, ModelForm

from sendinel.backend.models import InfoMessage

class InforServiceForm(ModelForm):
    
    name = CharField(max_length = 255, label = "Infoservice Name")
    
    class Meta:
        model = InfoMessage
        exclude = ['recipient']
        fields = ['name']