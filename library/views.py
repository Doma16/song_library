from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Song

def home(request):
    return render(request, template_name='library/home.html')

class SongsListView(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'library/home.html'
