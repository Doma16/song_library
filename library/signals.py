from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Song

from song_library.settings import GENIUS_TOKEN 

from django.core.files.base import ContentFile
from pytube import YouTube
import requests
from PIL import Image
from io import BytesIO
from lyricsgenius import Genius
import os

@receiver(post_save, sender=Song)
def update_song_image(sender, instance:Song, **kwargs):

    if instance.link != '' and os.path.basename(instance.image.url) == 'default_song.png':
        yt = YouTube(instance.link)
        genius = Genius(GENIUS_TOKEN)
        img_url = yt.thumbnail_url
        song_title = yt.title 

        sng = genius.search_song(title=song_title)

        img_lyr = sng.lyrics
        img_url = sng.song_art_image_thumbnail_url

        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True

            im = Image.open(r.raw)

            h, w = 125, 125
            if im.height > h and im.width > w:
                im.thumbnail((h,w))
            
            f = BytesIO()
            try:
                im.save(f, format='png')
                content = ContentFile(f.getvalue())
                name = ''.join(instance.title.strip().split())
                name = name + '.png'
                instance.lyrics = img_lyr
                instance.image.save(name=name, content=content)
            finally:
                f.close()
