from django.conf.urls.defaults import *
from sendinel.web.views import *

urlpatterns = patterns("",
    url(r"^$", 'sendinel.staff.views.index', name = 'index')
    )