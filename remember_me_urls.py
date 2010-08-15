import os

from django.conf import settings
from django.conf.urls.defaults import *  # pylint: disable-msg=W0401,W0614
from django.contrib import admin
from django.views.static import serve

import minerva.urls
import user_management.urls

admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'', include(minerva.urls)),
    (r'', include(user_management.urls)),
)

if settings.DEV_MODE:
    urlpatterns += patterns("",
        (r'^static/(.*)$', serve,
                {'document_root': os.path.join(settings.FILE_ROOT, "static/")}),
        )

