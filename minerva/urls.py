from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views

urlpatterns = patterns('',
    (r'^$', views.question),
)
