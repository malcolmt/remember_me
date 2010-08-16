from django import forms

from general import form_helpers
from minerva.models import UserProfile, Language

class QuestionForm(forms.Form):
    meta = forms.CharField(widget=forms.HiddenInput)
    answer = forms.ChoiceField(label="Meaning?", choices=(),
            widget=forms.RadioSelect(
                renderer=form_helpers.RadioFieldRenderer,
                attrs={"render_class": "multichoice"}))

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        answers = kwargs.pop('answers', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        # FIXME: This is a little hack-tastic. Maybe we get this from meta and
        # meta will always be present (either initial data or from form).
        if answers:
            self.fields['answer'].choices = answers
            if question:
                self.fields['meta'].initial = \
                        self._pack_meta_data(question, answers)

    def clean_meta(self):
        data = self.cleaned_data["meta"]
        # XXX: Hack (for now). This populates valid choice for "answer" before
        # it gets cleaned. Kind of an abuse of clean_FOO(), so I'll tidy it up
        # later.
        pieces = self._unpack_question_meta_data(data)
        self.fields["answer"].choices = [(bit, bit) for bit in pieces[1]]
        return pieces

    def _pack_meta_data(self, correct, possible_answers):
        """
        Flatten the question meta data so that we know which choices were
        presented to the user without having to store anything on the server.
        """
        data = [str(correct[0])]
        data.extend([str(item[0]) for item in possible_answers])
        return "|".join(data)
    
    def _unpack_question_meta_data(self, packed_data):
        data = [int(i) for i in packed_data.split("|")]
        return data[0], data[1:]

class UserProfileForm(forms.Form):
    language = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        language = kwargs.pop("language", None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["language"].choices = ([("", "<No preference>")] +
                list(Language.objects.values_list("code", "descriptive_name")))
        self.fields['language'].initial = language

