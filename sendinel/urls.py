from django.conf.urls.defaults import handler404, handler500, include, \
                                        patterns, url
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_web = {
    'packages': ('sendinel')
}

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'web/'}),
    (r'^groups/', include('sendinel.groups.urls')),
    (r'^infoservices/', include('sendinel.infoservices.urls')),
    (r'^medicine/', include('sendinel.medicine.urls')),
    (r'^web/', include('sendinel.web.urls')),
    (r'^notifications/', include('sendinel.notifications.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/', 'django.views.i18n.javascript_catalog', js_info_web,
        name = "jsi18n"),
    # (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

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

