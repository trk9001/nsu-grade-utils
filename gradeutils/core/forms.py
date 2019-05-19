from django import forms

from . import models


class TrimesterCreateForm(forms.ModelForm):

    class Meta:
        model = models.Trimester
        fields = ['student', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'disabled': True})
