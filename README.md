# Spotify Playlist by Album Cover Hue
This little project lets you create a new Spotify playlist where the songs from any other playlist are sorted by the dominant color of their album covers.
The script pulls album covers with the Spotify API, analyzes the main color of each cover and then arranges the tracks in the playlist based on this color order, giving you a visually unique music experience.
#### NOTES
- The code is far from perfect, and any help would not only be welcomed but also greatly appreciated
- Big thanks to [Minervoo](https://github.com/minervoo) for the help!!

### HOW TO USE THE CODE
- Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
- Create a new app with the Redirect URI "http://127.0.0.1:8888/callback" (the other options are not relevant)
- Download the [SpotifyColorSorting.py file](https://github.com/armeliens/SpotifyColorSorting/blob/main/SpotifyColorSorting.py) (the download button is on the top right of the code)
- Run the script and provide the "CLIENT_ID" and "CLIENT_SECRET" from the new app you just created when asked

### RESULT
- Playlist created: [link](https://open.spotify.com/playlist/7KcaZp49FUo84UmSiXXsEm?si=bf4aa6cf28064061)
- Time: the code spent about 7min making it

### VISUAL RESULT
![Visual result](https://github.com/armeliens/SpotifyColorSorting/blob/main/Visual%20result.png)

### METHODS FOR SORTING TO CHECK OUT
#### Most Common Color
- Pro: Simple and fast to compute; captures the most dominant hue in an image.
- Con: Fails with images that have multiple strong colors—only one dominant color is considered.
#### Average Color
- Pro: Very efficient; provides a rough “summary” color of the entire image.
- Con: Visually misleading in images with contrasting halves (e.g., blue + orange = brown-ish).
#### Supervised Learning
- Pro: Allows sorting based on human-defined categories or aesthetics; flexible and powerful.
- Con: Requires labeled data and training; results may depend heavily on subjective criteria.
#### LAB / OkLAB / OkLCH
- Pro: Perceptually uniform—color distances reflect how humans perceive color differences.
- Con: More complex to implement and requires color space conversion.
#### Gamma / sRGB Encoding
- Pro: Proper decoding ensures accurate averaging, blending, and comparison of colors.
- Con: Often overlooked—working directly in sRGB without gamma correction can yield incorrect results.
#### Color Quantization
- Pro: Extracts a compact set of representative colors; great for clustering or palette-based sorting.
- Con: Ignores spatial structure and can miss subtle tonal differences.

### TO DO LIST
- Color-themed mini playlists
- Command line tool

### Help me make Spotify see this idea be implemented
#### https://community.spotify.com/t5/Live-Ideas/Sorting-songs-by-album-cover-s-colors/idi-p/6897183#M315934
