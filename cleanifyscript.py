import sys
import spotipy
import spotipy.util as util
import math
from creds import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

def initializeAPI():
    #username = input("Enter your username: ")
    scope = "playlist-modify-private playlist-read-collaborative playlist-modify-public playlist-read-private"
    #token = util.prompt_for_user_token("parthesh123", scope,  client, secret, uri)
    #sp = spotipy.Spotify(token)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri= "http://localhost:8080" ,scope=scope)) 
    return sp

def getPlaylist(sp,inputUri):
    #playlistURI = input("Enter playlist URI of playlist you would like cleaned: ")
    username = sp.me().get('id')
    playlistURI = inputUri
    cleanName = sp.playlist(playlistURI).get('name') + " CLEAN"
    clean = sp.user_playlist_create(username ,name = cleanName, public=True, description="Made with Cleanify!")
    cleanId = clean.get('id')
    playlistId = sp.playlist(playlistURI).get('id')
    length = sp.playlist_tracks(playlistId, fields=None, limit=1, offset=0, market=None, additional_types=('track', )).get('total')
    iterations = math.ceil(length/100)
    n = 0
    for n in range (iterations):
        playlist = sp.playlist_tracks(playlistId, fields=None, limit=100, offset=(n*100), market=None, additional_types=('track', ))
        getSongs(playlist,sp,cleanId)
        n = n+1
    return clean.get('external_urls').get('spotify')

def getSongs(playlist,sp,cleanId):
    n = 0
    for track in range(len(playlist.get('items'))):
        title = playlist.get('items')[track].get('track').get('name')
        explicit = playlist.get('items')[track].get('track').get('explicit')
        artist = playlist.get('items')[track].get('track').get('artists')[0].get('name')
        album = playlist.get('items')[track].get('track').get('album').get('name')
        results = searchSong(title, artist, sp)
        getClean(results,sp,title,artist,cleanId,n)


def searchSong(title, artist, sp):
    search = title + " " + artist
    results = sp.search(search, limit = 15, offset = 0, type = 'track', market = None)
    return results

def getClean(results, sp, title, artist,cleanId,n):
    for track in range(len(results.get('tracks').get('items'))):
        rTitle = results.get('tracks').get('items')[track].get('name')
        rExplicit = results.get('tracks').get('items')[track].get('explicit')
        rArtist = results.get('tracks').get('items')[track].get('artists')[0].get('name')
        trackId = [results.get('tracks').get('items')[track].get('id')]
        if (rTitle == title and rArtist == artist and rExplicit == False):
            sp.user_playlist_add_tracks(sp.me().get('id'), cleanId, trackId)
            print(title + " " + "IS FOUND")
            return True
    print(title + "NOT FOUND")
    return False
    
