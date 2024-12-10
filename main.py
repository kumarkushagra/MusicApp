from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from downloadSongs import download
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"],
)

LIBRARY_FOLDER = os.path.join(os.getcwd(), "library")

# Configure templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/library", StaticFiles(directory="library"), name="library")
templates = Jinja2Templates(directory="templates")

# Pydantic models
class SongRequest(BaseModel):
    url: str

# Routes for serving HTML pages
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/songs")
async def get_songs():
    try:
        songs = [f for f in os.listdir(LIBRARY_FOLDER) if f.endswith('.mp3')]
        return JSONResponse(content=songs)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.get("/song-request", response_class=HTMLResponse)
async def request_song_page(request: Request):
    return templates.TemplateResponse("song_request.html", {"request": request})

@app.post("/song-request")
async def request_song(request: SongRequest):
    print("Received URL:", request.url)  # Log the incoming URL to verify it's reaching here.
    success = download.main(request.url)
    if success:
        return {"message": "Song downloaded successfully!"}
    else:
        raise HTTPException(status_code=500, detail="Failed to download song.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
