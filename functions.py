from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import random

app = FastAPI()

# Serve static files (e.g., CSS, JS, music files)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/library", StaticFiles(directory="library"), name="library")

# Define data structures for songs and playlists
class Playlist(BaseModel):
    id: int
    name: str
    songs: list[str]

class Song(BaseModel):
    name: str

# Example song data (this can be dynamically loaded from a database)
songs = ["song1.mp3", "song2.mp3", "song3.mp3", "song4.mp3", "song5.mp3"]
playlists = [
    Playlist(id=1, name="All Songs", songs=songs),
    Playlist(id=2, name="Favorites", songs=["song2.mp3", "song4.mp3"])
]

# Store current playlist and song index
current_playlist = playlists[0]  # Default to "All Songs"
current_song_index = 0
shuffle_mode = False

@app.get("/", response_class=HTMLResponse)
async def home():
    # Serve the HTML page
    with open("index.html", "r") as file:
        return file.read()

@app.get("/songs")
async def get_songs():
    # Return a list of all songs
    return songs

@app.get("/playlists")
async def get_playlists():
    # Return a list of all playlists
    return [playlist.dict() for playlist in playlists]

@app.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: int):
    # Return the playlist by ID
    playlist = next((p for p in playlists if p.id == playlist_id), None)
    if playlist:
        return playlist.dict()
    raise HTTPException(status_code=404, detail="Playlist not found")

@app.post("/playlist/{playlist_id}/add-song")
async def add_song_to_playlist(playlist_id: int, song: Song):
    # Add a song to the playlist
    playlist = next((p for p in playlists if p.id == playlist_id), None)
    if playlist:
        playlist.songs.append(song.name)
        return {"message": f"Song '{song.name}' added to playlist '{playlist.name}'"}
    raise HTTPException(status_code=404, detail="Playlist not found")

@app.get("/current-song")
async def get_current_song():
    # Return the current song being played
    return {"song": current_playlist.songs[current_song_index]}

@app.post("/next-song")
async def next_song():
    global current_song_index
    if shuffle_mode:
        current_song_index = random.randint(0, len(current_playlist.songs) - 1)
    else:
        current_song_index = (current_song_index + 1) % len(current_playlist.songs)
    return {"song": current_playlist.songs[current_song_index]}

@app.post("/previous-song")
async def previous_song():
    global current_song_index
    if shuffle_mode:
        current_song_index = random.randint(0, len(current_playlist.songs) - 1)
    else:
        current_song_index = (current_song_index - 1 + len(current_playlist.songs)) % len(current_playlist.songs)
    return {"song": current_playlist.songs[current_song_index]}

@app.post("/toggle-shuffle")
async def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode
    return {"shuffle": shuffle_mode}

@app.get("/current-playlist")
async def get_current_playlist():
    # Return the current playlist details
    return {"playlist": current_playlist.name}

@app.get("/library/{song_name}")
async def get_song_file(song_name: str):
    # Serve the requested song file
    song_path = os.path.join("library", song_name)
    if os.path.exists(song_path):
        return FileResponse(song_path)
    raise HTTPException(status_code=404, detail="Song not found")
