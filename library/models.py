from django.db import models
from django.contrib.auth.models import User

from pytube import YouTube
import requests, shutil
from PIL import Image

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    link = models.URLField(blank=True)
    image = models.ImageField(default='default_song.png', upload_to='song_pics')
    content = models.TextField(name='lyrics')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by: {self.author}'
    
    '''
    def save(self, *args, **kwargs):        
        super().save(*args, **kwargs)
        
    '''
    '''
        yt = YouTube(self.link)
        img_url = yt.thumbnail_url
        
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(self.image.path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        img = Image.open(self.image.path)
        
        h, w = 125, 125
        if img.height > h and img.width > w:
            img.thumbnail((h,w))
            img.save(self.image.path)
    '''
    
