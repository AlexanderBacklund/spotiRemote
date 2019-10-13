#!/usr/bin/env python
import sys
import spotipy
import spotipy.util as util
import time
import spotify_token as st
import evdev
#import argparse
import os

def setup():
    ''' parser = argparse.ArgumentParser()
    parser.add_argument('username', help='Spotify username')
    parser.add_argument('password', help='password')
    return parser.parse_args()'''
    user = os.environ['SPOTIFY_USER']
    password = os.environ['SPOTIFY_PASS']
    return user,password

def access_token(username, password):
    #try:
    data = st.start_session(username, password)
    #except Exception as e:
    #    print(e)
    #    print("did not connect to spotify try to log in again")
    #    return
    token = data[0]
    expiration_date = data[1]
    return token

def currently_played_Song(sp):
    if (sp):
        current = sp.currently_playing()
        print("currently played song is: " + current['item']['name'])
        print("The following artist: ")
        for artist in current["item"]['artists']:
            print(artist['name'])

    else:
        print("invalid token or no token")

def next_song(sp):
    if(sp and sp.currently_playing()):
        sp.next_track()
    else:
        print(" next song no token or spotify")

def prev_song(sp):
    if(sp and sp.currently_playing()):
        sp.previous_track()
    else:
        print("prev no token or spotify")

def play_pause(sp):
    if(sp and sp.currently_playing()):
        if sp.currently_playing()['is_playing']:
            sp.pause_playback()
        else:
            sp.start_playback()
    else:
        print("play pause no token or spotify")

def key_controller(sp):
    device = evdev.InputDevice('/dev/input/event4')
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if(event.code == 66 and event.value == 00):
                prev_song(sp)
            if(event.code == 67 and event.value == 00):
                next_song(sp)
            if(event.code == 61 and event.value == 00):
                play_pause(sp)

def main():
    username, password = setup()
    print(username)
    token = access_token(username, password)
    sp = spotipy.Spotify(auth=token)
    key_controller(sp)

if __name__ == '__main__':
    main()
