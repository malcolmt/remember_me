from django.conf.urls.defaults import *  # pylint: disable-msg=W0401,W0614
from django.contrib.auth import views as auth_views
from user_management import views as user_views

urlpatterns = patterns("",
    url("login/$", auth_views.login,
        {"template_name": "user_management/login.html"}, name="login"),
    url("logout/$", auth_views.logout, {"next_page": "/"}, name="logout"),
    url("create/$", user_views.create, name="create"),
)

