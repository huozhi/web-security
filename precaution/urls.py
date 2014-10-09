from django.conf.urls import patterns, include, url
from precaution import settings
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'precaution.views.index', name="index"),
    url(r'^board/$', 'message.views.board', name="message_board"),

    url(r'^xss/script/$', 'precaution.views.xss_script' ,name="xss_script_default"),
    url(r'^xss/script/(?P<data>.*)/', 'precaution.views.xss_script' ,name="xss_script"),

) + static(

    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT

) + static(

    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT

)
