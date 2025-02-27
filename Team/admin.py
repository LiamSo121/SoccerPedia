from django.contrib import admin

# Register your models here.
from .models import Team,YoutubeVideo,Review
# Register your models here.
admin.site.register(Team)
admin.site.register(YoutubeVideo)
admin.site.register(Review)
