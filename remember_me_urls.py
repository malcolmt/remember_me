from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.static import serve
import os
import minerva.urls

admin.autodiscover()

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(.*)$', serve, {'document_root': os.path.join(CURRENT_DIR, "static/")}),
    (r'^$', include(minerva.urls)),
)

