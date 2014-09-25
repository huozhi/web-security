from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'precaution.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'precaution.views.index', name="index"),
    url(r'^xss/$', 'message.views.home', name="message_home"),
    url(r'^primary/', 'precaution.views.primary_xss' ,name="primary_xss"),
    url(r'^primary/(?P<data>.*)/$', 'precaution.views.primary_xss' ,name="primary_xss"),
)
