# Generated by Django 4.2.2 on 2023-08-02 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_song_link"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="song",
            name="link",
        ),
    ]
