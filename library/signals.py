from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Song

from django.core.files.base import ContentFile
from pytube import YouTube
import requests
from PIL import Image
from io import BytesIO

@receiver(post_save, sender=Song)
def update_song_image(sender, instance:Song, **kwargs):

    if instance.link != '' and instance.image.name == 'default_song.png':
        yt = YouTube(instance.link)
        img_url = yt.thumbnail_url

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
                instance.image.save(name=name, content=content)
            finally:
                f.close()
