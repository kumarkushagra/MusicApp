from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import json
import uuid

from downloadSongs import download

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/library", StaticFiles(directory="library"), name="library")
templates = Jinja2Templates(directory="templates")

# Paths
LIBRARY_FOLDER = 'library'
PLAYLISTS_FILE = 'playlists.json'

# Ensure library and playlists file exist
os.makedirs(LIBRARY_FOLDER, exist_ok=True)
if not os.path.exists(PLAYLISTS_FILE):
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump([], f)

# Pydantic models
class SongRequest(BaseModel):
    url: str

class Playlist(BaseModel):
    id: str = str(uuid.uuid4())
    name: str
    songs: List[str] = []

# Routes for serving HTML pages
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/request-song", response_class=HTMLResponse)
async def request_song_page(request: Request):
    return templates.TemplateResponse("request_song.html", {"request": request})

@app.get("/playlists", response_class=HTMLResponse)
async def playlists_page(request: Request):
    with open(PLAYLISTS_FILE, 'r') as f:
        playlists = json.load(f)
    return templates.TemplateResponse("playlists.html", {"request": request, "playlists": playlists})

# Song and Playlist Management Routes
@app.get("/songs")
async def get_songs():
    try:
        songs = [f for f in os.listdir(LIBRARY_FOLDER) if f.endswith('.mp3')]
        return JSONResponse(content=songs)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/request-song")
async def request_song(request: SongRequest):
    url = request.url
    try:
        success = download.main(url)
        if success:
            return {"message": "Song downloaded successfully!"}
        else:
            raise HTTPException(status_code=500, detail="Failed to download song.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

@app.post("/create-playlist")
async def create_playlist(playlist: Playlist):
    try:
        with open(PLAYLISTS_FILE, "r") as f:
            playlists = json.load(f)
        
        # Check if playlist with same name exists
        if any(p['name'] == playlist.name for p in playlists):
            raise HTTPException(status_code=400, detail="Playlist name already exists")
        
        playlists.append(playlist.dict())
        
        with open(PLAYLISTS_FILE, "w") as f:
            json.dump(playlists, f, indent=2)
        
        return {"message": "Playlist created successfully", "playlist_id": playlist.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating playlist: {e}")

@app.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: str):
    try:
        with open(PLAYLISTS_FILE, "r") as f:
            playlists = json.load(f)
        
        playlist = next((p for p in playlists if p['id'] == playlist_id), None)
        if playlist:
            return playlist
        raise HTTPException(status_code=404, detail="Playlist not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving playlist: {e}")

@app.post("/playlist/{playlist_id}/add-song")
async def add_song_to_playlist(playlist_id: str, song: str):
    try:
        with open(PLAYLISTS_FILE, "r") as f:
            playlists = json.load(f)
        
        for playlist in playlists:
            if playlist['id'] == playlist_id:
                if song not in playlist['songs']:
                    playlist['songs'].append(song)
                    break
        
        with open(PLAYLISTS_FILE, "w") as f:
            json.dump(playlists, f, indent=2)
        
        return {"message": "Song added to playlist successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding song to playlist: {e}")

@app.delete("/playlist/{playlist_id}")
async def delete_playlist(playlist_id: str):
    try:
        with open(PLAYLISTS_FILE, "r") as f:
            playlists = json.load(f)
        
        playlists = [p for p in playlists if p['id'] != playlist_id]
        
        with open(PLAYLISTS_FILE, "w") as f:
            json.dump(playlists, f, indent=2)
        
        return {"message": "Playlist deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting playlist: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
