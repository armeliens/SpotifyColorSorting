import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from io import BytesIO
from PIL import Image
import colorsys

def get_saved_tracks(sp):
    tracks = []
    results = sp.current_user_saved_tracks()
    while results:
        for item in results['items']:
            track = item['track']
            image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
            tracks.append((track['id'], track['name'], image_url))
        results = sp.next(results) if results['next'] else None
    return tracks

def get_dominant_hue(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert('RGB')
    image = image.resize((50, 50))
    pixels = list(image.getdata())
    avg_color = tuple(sum(c) // len(c) for c in zip(*pixels))
    hue, _, _ = colorsys.rgb_to_hsv(avg_color[0] / 255.0, avg_color[1] / 255.0, avg_color[2] / 255.0)
    return hue

def create_ordered_playlist(sp, user_id, tracks):
    playlist = sp.user_playlist_create(user_id, "Sorted by Cover Hue", public=False)
    track_ids = [track[0] for track in tracks]
    chunk_size = 100
    for i in range(0, len(track_ids), chunk_size):
        chunk = track_ids[i:i + chunk_size]
        sp.playlist_add_items(playlist['id'], chunk)
    print("Playlist created successfully!")

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-library-read playlist-modify-private"
    ))
    
    user_id = sp.me()['id']
    
    tracks = get_saved_tracks(sp)
    tracks_with_hue = [(t[0], t[1], get_dominant_hue(t[2])) for t in tracks if t[2]]
    tracks_with_hue.sort(key=lambda x: x[2])
    
    create_ordered_playlist(sp, user_id, tracks_with_hue)

if __name__ == "__main__":
    main()
