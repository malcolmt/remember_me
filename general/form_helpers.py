from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class RadioFieldRenderer(widgets.RadioFieldRenderer):
    """
    A version of the standard RadioFieldRenderer class that labels the rendered
    list with an identifiable class (via the render_class attr). Usage is
    something like:

        forms.ChoiceField(...,
                widget=forms.RadioSelect(renderer=RadioFieldRenderer,
                    attrs={"render_class": "multichoice"}))
    """

    def __init__(self, name, value, attrs, choices):
        self.render_class = attrs.pop("render_class", "")
        super(RadioFieldRenderer, self).__init__(name, value, attrs, choices)

    def render(self):
        return mark_safe(u'<ul class="%s">\n%s\n</ul>' %
                (self.render_class,
                u'\n'.join([u'<li>%s</li>' % force_unicode(w) for w in self])))


