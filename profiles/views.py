from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, NewSongLinkForm, NewSongNoLinkForm

from library.models import Song
from pytube import YouTube

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'profiles/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profiles/profile.html', context)

@login_required
def new_song(request):
    if request.method == 'POST':
        l_form = NewSongLinkForm(request.POST)
        nl_form = NewSongNoLinkForm(request.POST)

        if l_form.is_valid():
            link = request.POST['link']
            yt = YouTube(link)

            title = yt.vid_info['videoDetails']['title']
            author = yt.vid_info['videoDetails']['author']
            content = ''
            user = request.user

            s = Song(title=title, author=author, link=link, user=user)
            s.lyrics = content
            s.save()

            return redirect('song_added')

        elif nl_form.is_valid():
            breakpoint()
            
    else:
        l_form = NewSongLinkForm()
        nl_form = NewSongNoLinkForm()

    context = {
        'l_form': l_form,
        'nl_form': nl_form,
    }

    return render(request, 'profiles/new_song.html', context)


def song_added(request):
    return render(request, 'profiles/song_added.html' )