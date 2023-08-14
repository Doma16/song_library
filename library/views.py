from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import Song

def home(request):
    return render(request, template_name='library/home.html')

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