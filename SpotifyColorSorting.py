import subprocess
import sys

required_libraries = ["spotipy", "requests", "colorthief", "matplotlib", "numpy", "rich"]
for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        print(f"Library '{lib}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from colorthief import ColorThief
from matplotlib import colors
import numpy as np
import os
from rich.progress import Progress, BarColumn, TimeElapsedColumn, SpinnerColumn, TextColumn
from rich.live import Live
import math

if os.path.exists("credentials.txt"):
    with open("credentials.txt", "r") as cred_file:
        lines = cred_file.readlines()
        CLIENT_ID = lines[0].strip().split("=")[1]
        CLIENT_SECRET = lines[1].strip().split("=")[1]
else:
    while True:
        CLIENT_ID = input("Please enter your Spotify Client ID: ").strip()
        CLIENT_SECRET = input("Please enter your Spotify Client Secret: ").strip()
        
        # validate the credentials by attempting to create a SpotifyOAuth object
        try:
            SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://127.0.0.1:8888/callback')
            break
        except Exception as e:
            print(f"Invalid credentials. Please try again. Error: {e}")

# save the credentials to a file for future use
with open("credentials.txt", "w") as cred_file:
    cred_file.write(f"SPOTIFY_CLIENT_ID={CLIENT_ID}\n")
    cred_file.write(f"SPOTIFY_CLIENT_SECRET={CLIENT_SECRET}\n")
playlist_link = input("Please enter the Spotify playlist link: ").strip()
if not playlist_link.startswith("https://open.spotify.com/playlist/"):
    raise ValueError("Invalid playlist link. Please provide a valid Spotify playlist URL.")
PLAYLIST_ID = playlist_link.split("/")[-1].split("?")[0]
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = "playlist-modify-public playlist-modify-private user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def get_tracks_from_playlist(playlist_id):
    print(f"Fetching tracks...")
    tracks = []
    offset = 0
    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset)
        tracks.extend(results['items'])
        if len(results['items']) < 100:
            break
        offset += 100
    print(f"Total tracks fetched: {len(tracks)}")
    return tracks

def get_dominant_color(image_url):
    response = requests.get(image_url)
    with open('temp_image.jpg', 'wb') as file:
        file.write(response.content)
    
    color_thief = ColorThief('temp_image.jpg')
    dominant_color = color_thief.get_color(quality=1)
    hsl_color = rgb_to_hsl(dominant_color)
    return hsl_color

def rgb_to_hsl(rgb):
    rgb = np.array(rgb) / 255.0
    h, s, v = colors.rgb_to_hsv(rgb)  
    l = (2 - s) * v / 2
    if l != 0:
        s = (2 * (1 - l / v)) * s
    h = h * 360
    s = s * 100
    l = l * 100
    hsl = (h, s, l)
    return hsl

def sort_tracks_by_color(tracks, progress, task):
    track_colors = []

    for track in tracks:
        album = track['track']['album']
        image_url = album['images'][0]['url']
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        
        print(f"Processing: {track_name} - {artist_name}")
        dominant_color = get_dominant_color(image_url)
        track_colors.append((track, dominant_color))
        progress.update(task, description="Sorting by color")
        progress.advance(task)

    # Sort by hue, then by lightness, then by saturation for better color grouping
    sorted_tracks = sorted(
        track_colors,
        key=lambda x: (x[1][0], x[1][2], x[1][1])  # (hue, lightness, saturation)
    )
    return [track[0] for track in sorted_tracks]


def create_sorted_playlist(sorted_tracks, progress, task):
    print("Creating a new playlist sorted by color...")
    user_id = sp.current_user()['id']
    original_playlist = sp.playlist(PLAYLIST_ID)
    original_name = original_playlist['name']
    new_playlist_name = f"{original_name} - Ordered by Color"
    playlist = sp.user_playlist_create(user_id, new_playlist_name, public=True)
    playlist_id = playlist['id']
    print(f"Created playlist with ID: {playlist_id}")

    for i in range(0, len(sorted_tracks), 100):
        track_ids = [track['track']['id'] for track in sorted_tracks[i:i+100]]
        print(f"Adding {len(track_ids)} tracks to playlist...")
        sp.playlist_add_items(playlist_id, track_ids)
        progress.update(task, description="Uploading to playlist")
        progress.advance(task)


def main():
    print("Counting tracks...")
    tracks = get_tracks_from_playlist(PLAYLIST_ID)
    num_tracks = len(tracks)
    playlist_chunks = math.ceil(num_tracks / 100)

    total_steps = 1 + num_tracks + playlist_chunks + 1  # fetch + sort + upload + done

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
    )

    with Live(progress, refresh_per_second=20, screen=False):
        task = progress.add_task("Starting...", total=total_steps)

        progress.update(task, description="Fetched playlist")
        progress.advance(task)

        sorted_tracks = sort_tracks_by_color(tracks, progress, task)
        create_sorted_playlist(sorted_tracks, progress, task)
        progress.update(task, description="Finishing...")
        progress.advance(task)

    print("All done!")

    
if __name__ == '__main__':
    main()
