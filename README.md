# 🎨 Spotify Playlist by Album Cover Color

This project lets you create a **Spotify playlist where songs are sorted by the dominant color of their album covers**.  
By pulling album art via the Spotify API, the script analyzes each cover’s main hue and reorders the tracks accordingly — offering a uniquely visual music experience.

---

### 💡 Overview

- Uses the Spotify API to fetch album covers from any playlist
- Analyzes each cover’s dominant color
- Creates a new playlist with the songs sorted by hue

---

### 🚀 Getting Started

1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Create a new app with the **Redirect URI**:  
   `http://127.0.0.1:8888/callback`
3. Download the [`SpotifyColorSorting.py`](https://github.com/armeliens/SpotifyColorSorting/blob/main/SpotifyColorSorting.py) script  
   *(Click the "Download" button in the top-right corner of the file)*
4. Double-click on the file you just downloaded
5. When prompted, enter your `CLIENT_ID` and your `CLIENT_SECRET` from the Spotify Developers app you just created

---

### ✅ Example Result

- 🟢 Playlist created: [example](https://open.spotify.com/playlist/7kIIr7qSbFNbkbKw4treKc?si=8cd43c6055cf418a)
- 🕒 Time taken: ~7 minutes for a 357 tracks long playlist
- 📸 Visual preview

  ![Visual result](https://github.com/armeliens/SpotifyColorSorting/blob/main/Visual%20result.png)

---

### 🎨 Sorting Methods (Used or Under Consideration)

#### 🔹 Most Common Color
- ✅ **Pro**: Fast and simple; captures the dominant hue.
- ❌ **Con**: Doesn’t work well with covers that feature multiple vibrant colors.

#### 🔹 Average Color
- ✅ **Pro**: Extremely efficient; gives a general tone of the image.
- ❌ **Con**: Misleading when strong color contrasts are present.

#### 🔹 Supervised Learning
- ✅ **Pro**: Can sort by aesthetic rules or categories.
- ❌ **Con**: Requires labeled training data and human input.

#### 🔹 LAB / OkLAB / OkLCH
- ✅ **Pro**: Matches human color perception more accurately.
- ❌ **Con**: More complex to implement due to color space conversion.

#### 🔹 Gamma / sRGB Encoding
- ✅ **Pro**: Ensures accurate color representation when averaging.
- ❌ **Con**: Often overlooked; improper usage can skew results.

#### 🔹 Color Quantization
- ✅ **Pro**: Ideal for extracting a small palette of representative colors.
- ❌ **Con**: May miss subtle details or ignore layout/context of the cover.

---

### 🛠️ To-Do List

- [X] Progress bar with %
- [ ] Color-themed mini playlists
- [ ] Command-line version
- [ ] Collage picture maker (like [Discover Quickly](https://discoverquickly.com/))

---

### 🙌 Contributing

The code is far from perfect and **any help is more than welcome!**  
Big thanks to [Minervoo](https://github.com/minervoo) for their contributions! ❤️

---

### 📢 Want to See This Feature in Spotify?

Help support the idea by upvoting it here:  
[Sorting songs by album cover colors (Spotify Community Idea)](https://community.spotify.com/t5/Live-Ideas/Sorting-songs-by-album-cover-s-colors/idi-p/6897183#M315934)
