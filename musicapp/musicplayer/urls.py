from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('favorites',views.favorites,name='favorites'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('onrepeat',views.onrepeat,name='onrepeat'),
    path('artists',views.artists,name='artists'),
    path('albums',views.albums,name='albums'),
    path('songs',views.songs,name='songs'),
    path('playlists',views.playlists,name='playlists'),
    path('like',views.like,name='like'),
    path('addtoplaylist',views.albums,name='addtoplaylist'),
    path('playlistsongs',views.playlistsongs,name='playlistsongs'),
    path('deletelike',views.deletelike,name='deletelike'),
    path('albumsongs',views.albumsongs,name='albumsongs'),
    path('artistsongs',views.artistsongs,name='artistsongs'),
    path('createplaylist',views.createplaylist,name='createplaylist'),
    path('existingplaylist',views.existingplaylist,name='existingplaylist'),
    path('addsong',views.addsong,name='addsong'),
    path('localsong',views.localsong,name='localsong'),
    path('process-song',views.process_song,name='process-song'),
    path('sho',views.sho,name='sho'),
    
]