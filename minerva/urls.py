from django.conf.urls.defaults import *  # pylint: disable-msg=W0401,W0614
from django.views.generic.simple import direct_to_template

from minerva import views


urlpatterns = patterns('',
    url(r'^/$', views.question),
    url("test/$", direct_to_template,
        {"template": "minerva/test_display.html"}),
)

