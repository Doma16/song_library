from django.urls import path
from . import views
from .views import SongsListView

urlpatterns = [
    path("", SongsListView.as_view(), name="home"),
]
