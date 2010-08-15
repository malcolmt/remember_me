from django import template
from django.contrib.auth import forms

register = template.Library()

@register.inclusion_tag("user_management/login_form.html")
def login_form(style=None):
    context = {"form": forms.AuthenticationForm()}
    if style != "visible":
        context["hidden"] = True
    return context

