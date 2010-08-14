from django.conf.urls.defaults import *  # pylint: disable-msg=W0401,W0614

from minerva import views


urlpatterns = patterns('',
    (r'^$', views.question),
)

