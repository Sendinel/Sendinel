from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'web/'}),
    (r'^web/', include('sendinel.web.urls')),
    (r'^staff/', include('sendinel.staff.urls')),    
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    # Example:
    # (r'^sendinel/', include('sendinel.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)), 
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^mediaweb/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

