from django import forms

from . import models


class TrimesterCreateForm(forms.ModelForm):

    student = forms.ModelChoiceField(
        queryset=models.Student.objects.all(),
        widget=forms.HiddenInput,
        to_field_name='slug',
        required=True,
    )

    class Meta:
        model = models.Trimester
        fields = ['student', 'code']
