# Generated by Django 5.1.4 on 2024-12-16 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the YouTube video', max_length=255)),
                ('url', models.URLField(help_text='YouTube video URL')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the video was added')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='youtube_videos', to='Team.team')),
            ],
        ),
    ]
