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

        img_lyr = f'[no lyrics for {song_title}]'
        if sng is not None:

            if check_artist(yt.author, sng.artist, song_title, sng.title):
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


def check_artist(aut1:str, aut2:str, tit1:str, tit2:str):

    aut1 = [ x.lower() for x in aut1 if x.isalpha() or x.isnumeric()]
    aut2 = [ x.lower() for x in aut2 if x.isalpha() or x.isnumeric()]
    tit1 = [ x.lower() for x in tit1 if x.isalpha() or x.isnumeric()]
    tit2 = [ x.lower() for x in tit2 if x.isalpha() or x.isnumeric()]

    word_len = 5
    if len(tit1) >= word_len:
        words = [''.join(tit1[i:i+word_len]) for i in range(0,len(tit1)-word_len,1)]
        tit2 = ''.join(tit2)

        for word in words:
            if tit2.find(word) > -1:
                return True 
    else:
        tit1 = ''.join(tit1)
        tit2 = ''.join(tit2)

        if tit1 == tit2:
            return True
        return False

    return False
