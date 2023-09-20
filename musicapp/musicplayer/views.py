from django.shortcuts import render,redirect
import os
from django.shortcuts import get_object_or_404
import mutagen
from django.contrib.auth.models import User
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
from mutagen.flac import FLAC
from django.db.models import Count
from django.http import HttpResponse
from mutagen.mp3 import MP3
from mutagen.mp3 import HeaderNotFoundError
from .models import audio as ssong
from .models import favorite as ffavorite
from .models import playlist as pplaylist
from .models import test 
from datetime import timedelta
import threading
import json 
from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
# Create your views here.

music_dir= r'C:\\Users\\DELL\\Desktop\\dns projects\\musicplayer\\musicapp\\static\\audio\\Musicplayer'
musicdir=r"C:\Users\DELL\Desktop\dns projects\musicplayer\musicapp\media"

# print(musicdir)
cwd = os.getcwd()

# Convert absolute path to relative path
# relative_path = os.path.relpath(musicdir, cwd)

# print(relative_path) 

def get_music_file(dir):
    global musicfiles
    musicfiles = os.listdir(dir)
    
    file_paths = []
    for file in musicfiles:
        file_path = os.path.join(dir, file)
        raw_file_path = r'{}'.format(file_path)
        file_paths.append(raw_file_path)
    return file_paths
        

pathss=get_music_file(musicdir)

def convertbinary(filepath):
    with open(filepath,'rb') as file:
        binarydata=file
        return binarydata

def writebinary(binarydata,filepathsss):
    with open(filepathsss,'wb') as musicbinary:
        musicbinary.write(binarydata)
    


# for data in musicfiles:
#     # print(data)
#     if data.endswith('.mp3'):
#         filteredsongs = [data]
#         file_filteredpaths = []
#         for file in filteredsongs:
            
#             file_path = os.path.join(musicdir, file)
#             # print(file_path)
#             raw_file_path = r'{}'.format(file_path)
#             file_filteredpaths.append(raw_file_path)
        
#             for mutatedsongs in file_filteredpaths:
#                 try:
#                     mutegensongs=MP3(mutatedsongs)
#                     artist = mutegensongs.get("TPE1")
#                     artiststring=str( mutegensongs.get("TPE1"))
#                     title = str(mutegensongs.get("TIT2"))
#                     length = mutegensongs.info.length
#                     album = str(mutegensongs.get("TALB"))
#                     duration = timedelta(seconds=length)
#                     duration_microseconds = (24 * 60 * 60 * duration.days + duration.seconds) * 1000000 + duration.microseconds
#                     # print(title)
#                     ssong.objects.create(name=title,album=album,artist=artiststring,length=duration,link=mutatedsongs)
#                     # print('fin')
                    
#                 except HeaderNotFoundError:
#                     print(f"{mutatedsongs} is not a valid MP3 file.")
#                 break
#             break
# print('fin')
                 

def home(request):
    
    song = ssong.objects.get(name='Relentless - SongsLover.com')
  
    context = {'song': song}
    
        
    return render(request,'home.html',context)

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        # print("inafikahahhdhadhvdhvhdahvdshvhsd")
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect ('login')
    else:
        return render(request,'login.html')
    
@login_required
def logout(request):
    auth.logout()
    return render('login')

def register(request):
    # test=ssong.objects.all()
    if request.method=='POST':
        firstname=request.POST['firstname']
        secondname=request.POST['secondname']
        username=request.POST['username']
        email=request.POST['email']
        
        password=request.POST['password']
        
       
        if User.objects.filter(email=email).exists():
            messages.info(request,'email already exists')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'user already exists')
            return redirect('register')
        
        else:
            User.objects.create_user(first_name=firstname,last_name=secondname,username=username,email=email,password=password)
            
            request.session['firstname'] = firstname
            request.session['username'] = username
            return redirect('login')
    else:
        return render(request,'register.html')#,#{'r':test}#)
@login_required
def onrepeat(request):
    return render(request,'onrepeat.html')
@login_required
def favorites(request):
    favor=ffavorite.objects.all()
    return render(request,'favorites.html', {'favor':favor} )
@login_required
def artists(request):
    artist = ssong.objects.values('artist').annotate(num_songs=Count('id')).order_by('artist')
    
    return render(request,'artists.html',{'artist':artist})

@login_required
def songs(request):
    songlist=ssong.objects.exclude(artist__exact='None')
    user_id = int(request.user.id)
    favoriteslist=ffavorite.objects.all()
    
    # allsongsid= request.GET.get('songid')
    if request.method=='POST':
        allsongsid=int(request.POST['songid'])
        if ffavorite.objects.filter(user_id=user_id, song_id=allsongsid).exists():
            pass
        else:
            changebool=get_object_or_404(ssong,pk=allsongsid)
            changebool.favorite_bool=True
            changebool.save()
            song=ssong.objects.get(pk=allsongsid)
            ffavorite.objects.create(song=song,user=request.user)
        
        
        return redirect('favorites')
        
    
    return render(request,'songs.html',{'song':songlist,'value':favoriteslist})

@login_required
def playlists(request):
    playlist=pplaylist.objects.all()
    if request.method=='POST':
        playlistname=request.POST['name']
        
        request.session['playlist_name'] = playlistname
        
        return redirect('playlistsongs')
    
    return render(request,'playlists.html',{'play':playlist})
@login_required
def albums(request):
    albums = ssong.objects.values('album').annotate(num_songs=Count('id')).order_by('album')
    
    return render(request,'albums.html',{'albums': albums})

def like(request):
    user_id = request.user.id
    
        #Add message here


    return render(request,'favorites.html',)

def createplaylist(request):
    if request.method=='POST':
        songid=request.session['addtoplaylistid']
        playlistname=request.POST['playlistname'] #check if playlist exists
        playlists=pplaylist.objects.all()
        song=ssong.objects.get(id=songid)
        pplaylist.objects.create(user=request.user,song=song,name=playlistname)
        
        return render(request,'playlists.html',{'playlists':playlists})

def addtoplaylist(request):
    if request.method=='POST':
        songid=int(request.POST['songid'])
        
        request.session['addtoplaylistid']=songid
        
        return redirect ('createplaylist')
    
    
    return render(request,'playlists.html')


def playlistsongs(request):
    playlist_name = str(request.session.get('playlist_name'))
    playlist = get_object_or_404(pplaylist, name=playlist_name)
    songs=playlist.song.all()
    return render(request,'playlistsongs.html',{'song':songs})
    


def deletelike(request):
    if request.method=='POST':
        id=request.POST['songid']
        songdelete=ffavorite.objects.get(id=id)
        songdelete.delete
        return redirect('favorites')
    return render(request,'favorites.html')

def albumsongs(request):
    if request.method=='POST':
        albumname=str(request.POST['albumname'])
        songs=ssong.objects.filter(album=albumname)
        
        return render(request,'albumsongs.html',{'song':songs})
        
def artistsongs(request):
    if request.method=='POST':
        artistname=request.POST['artistname']
        songs=ssong.objects.filter(artist=artistname)
        return render(request,'artistsongs.html',{'song':songs})
    

def existingplaylist(request):
    if request.method=='POST':
        songid=request.session['addtoplaylistid']
        # print(songid)
        existingplaylist=request.POST['existingplaylist']
        playlistgot=pplaylist.objects.get(id=existingplaylist)
        song=ssong.objects.get(id=songid)
        print(song)
        playlistgot.song.add(song)
        
def addsong(request):
    if request.method=='POST':
        songaudio=request.FILES.getlist('song')
        if len(songaudio)==1:
            song=songaudio[0]
            path=song.temporary_file_path()
            name=str(song.name)
            if name.endswith('.mp3'):
                test.objects.create(songlink=song.temporary_file_path())
                print(name)
                
                
            #     fs = FileSystemStorage()
            #     saved_file = fs.save('song', song)
            #     file_url = fs.url(saved_file)
            #     test.objects.create(song=file_url)
            # else:
            #     HttpResponse('not a mp3 file')
            #     return render(request,'addsong.html')
            # return redirect('localsong')
        else:
            for songlink in songaudio:
                name=str(songlink.name)
                print(name)
                
                if name.endswith('.mp3'):
                    test.objects.create(songlink=songlink)
                #     fs = FileSystemStorage()
                #     saved_file = fs.save('song', songlink)
                #     file_url = fs.url(saved_file)
                #     test.objects.create(song=file_url)
                # else:
                #     songnumber=songaudio.index(songlink)
                #     HttpResponse(songnumber + 'is not a mp3 file')
                #     return render(request,'addsong.html') 
            # return redirect('localsong')
    return render(request,'addsong.html')
                
            
                
                
                
            
            
    
    
    return render(request,'addsong.html')

def localsong(request):
    songlinks=test.objects.all()
    free=[]
    for link in songlinks:
        link=link.songlink
        free.append(link)
    context={'link':free}
    
    
    return render(request,'localsong.html',context)

def process_song(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        print(url)
        # Perform further processing with the URL if needed

        # Return a JSON response indicating the success status
        response_data = {'status': 'success'}
        return JsonResponse(response_data)
    
    # If the request method is not POST, return an error response
    response_data = {'status': 'error', 'message': 'Invalid request method'}
    return JsonResponse(response_data, status=400)
def sho(request):
    if request.method=='POST':
        song=request.FILES.get('song')
        
        hr=song.temporary_file_path()
        print(hr)

    return render(request,'test.html')