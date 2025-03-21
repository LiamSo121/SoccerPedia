# Generated by Django 5.1.4 on 2025-02-22 19:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('League', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year_of_foundation', models.IntegerField()),
                ('city', models.CharField(max_length=255)),
                ('stadium_name', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/team_logos/')),
                ('number_of_trophies', models.IntegerField(default=0)),
                ('website', models.URLField(blank=True, null=True)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='League.league')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.PositiveSmallIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=5)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='review_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_reviews', to='Team.team')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.TextField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the video was added')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='youtube_videos', to='Team.team')),
            ],
        ),
    ]
