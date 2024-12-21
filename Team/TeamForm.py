from django import forms
from django.forms import inlineformset_factory
from .models import Team, YoutubeVideo

# Create a formset for YoutubeVideos linked to a Team
class YoutubeVideoForm(forms.ModelForm):
    class Meta:
        model = YoutubeVideo
        fields = ['title', 'url']

# Create an inline formset for YouTube videos, linked to the Team model
YoutubeVideoFormSet = inlineformset_factory(
    Team, YoutubeVideo, form=YoutubeVideoForm, extra=2, can_delete=False
)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
