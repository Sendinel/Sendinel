from sendinel.settings import PROJECT_PATH
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.core import serializers

data = open(PROJECT_PATH + "/backend/fixtures/contenttype.json").read()
deserialized = serializers.deserialize("json", data)
object_dict = dict([[object.object.model, object.object.id] for object in deserialized if isinstance(object.object, ContentType)])

counter = 1000

def set_content_type_id(sender, **kwargs):
    content_type = kwargs.get('instance')
    new_id = object_dict.get(content_type.model, None)
    if new_id:
        content_type.pk = object_dict[content_type.model]
    else:
        global counter
        content_type.pk = counter
        counter += 1
pre_save.connect(set_content_type_id, sender=ContentType)
