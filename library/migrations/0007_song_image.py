# Generated by Django 4.2.2 on 2023-08-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0006_song_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="song",
            name="image",
            field=models.ImageField(default="default_song.png", upload_to="song_pics"),
        ),
    ]
