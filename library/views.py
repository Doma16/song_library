from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Song
from profiles.forms import NewSongNoLinkForm

def home(request):
    return render(request, template_name='library/home.html')

def song(request, **kwargs):

    context = {'song':Song.objects.get(id=kwargs['song_id'])}
    
    if request.method == 'POST':

        song_form = NewSongNoLinkForm(request.POST)
        if song_form.is_valid():
            context['song'].lyrics = request.POST['lyrics']
            context['song'].author = request.POST['author']
            context['song'].title = request.POST['title']
            context['song'].save()
            messages.success(request, f'Song updated!')
            return redirect('home')
        messages.error(request, f'Song not updated!')
        return redirect('home')
        
    else:
        song_form = NewSongNoLinkForm(instance=context['song'])

    context['song_form'] = song_form 
    return render(request, template_name='library/song.html', context=context)

class SongsListView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'library/home.html'

    paginate_by = 5


class ProfileSongsListView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'library/mylib.html'

    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        songs = Song.objects.filter(user=user)
        return songs