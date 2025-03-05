from django import forms
from .models import Cus


class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = "__all__"