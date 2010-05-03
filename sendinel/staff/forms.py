from django.forms import CharField, ModelForm, Textarea

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
        