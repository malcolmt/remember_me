from django.conf.urls.defaults import *  # pylint: disable-msg=W0401,W0614
from django.views.generic.simple import direct_to_template

from minerva import views


urlpatterns = patterns('',
    url(r"^$", views.question, name="question-page"),
    url(r"test/$", direct_to_template,
        {"template": "minerva/test_display.html"}, name="test-page"),
    url(r"stats/$", views.statistics, name="stats"),
)

