# Generated by Django 4.2.2 on 2023-08-02 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0007_song_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="link",
            field=models.URLField(blank=True),
        ),
    ]