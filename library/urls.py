from django.urls import path
from . import views
from .views import SongsListView, ProfileSongsListView

urlpatterns = [
    path("", SongsListView.as_view(), name="home"),
    path('my_library/', ProfileSongsListView.as_view(), name='mylib'),
]
