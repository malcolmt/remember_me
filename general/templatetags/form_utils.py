"""
Template tags for working with forms.
"""

from django.template import Library

register = Library()

@register.inclusion_tag("general/form_tag.html")
def form_layout(form, show_required=True):
    """
    Display a form using a standard layout fragment. If the "show-required"
    parameter is non-false, required fields will have an asterisk before their
    label.
    """
    return {"form": form, "show_required": show_required}

