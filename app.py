from pytube import YouTube, Playlist

def downloadYoutubeVideo(url, isOnlyAudio = False):
    '''Download a YouTube video or only audio.'''
    if isOnlyAudio:
        YouTube(url).streams.filter(only_audio=True)[0].download('downloads/audios')
    else:
        YouTube(url).streams.get_highest_resolution().download('downloads/videos')

def downloadYoutubePlaylist(playlist, isOnlyAudio = False):
    '''Download a YouTube playlist video or only audio.'''
    playlist = Playlist(playlist)
    for url in playlist:
        downloadYoutubeVideo(url, isOnlyAudio)

def downloadYoutubeLinks(links, isOnlyAudio = False):
    '''Download a YouTube link list (videos and playlists, in video format or audio)'''
    for link in links:
        if 'list' in link:
            downloadYoutubePlaylist(link, isOnlyAudio)
        else:
            downloadYoutubeVideo(link, isOnlyAudio)

# VERIFICAR PQ SÓ UM LINK DE PLAYLIST ESTÁ FUNCIONANDO.

#TESTs:
video = 'https://youtu.be/AvcQjOUuII0'
playlist = 'https://www.youtube.com/watch?v=NQiGW8kvI9M&list=PL0Tm-7v0aJQ1VfIfYtCEsFNnw5D6f99sL&ab_channel=LeandroCardoso'
links = ['https://www.youtube.com/watch?v=1-LlX64hAPA&list=RD1-LlX64hAPA&start_radio=1&ab_channel=GabyCastilho']

#downloadYoutubeVideo(video, True)
#downloadYoutubePlaylist(playlist, True)
#downloadYoutubeLinks(links, True)
print(Playlist(playlist))
print(Playlist('https://www.youtube.com/watch?v=1-LlX64hAPA&list=RD1-LlX64hAPA&start_radio=1&ab_channel=GabyCastilho'))
