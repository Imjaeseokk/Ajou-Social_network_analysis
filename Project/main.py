from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import csv
from pathlib import Path
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Path to the Client folder where HTML files are located
CLIENT_FOLDER = Path(__file__).parent / "Client"
templates = Jinja2Templates(directory=CLIENT_FOLDER)

# Path to the CSV file where selected songs will be stored
CSV_FILE = Path(__file__).parent / "selected_songs.csv"

# Ensure the CSV file exists and has a header
if not CSV_FILE.exists():
    with CSV_FILE.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Artist'])

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    # Render the main HTML page
    return templates.TemplateResponse('main.html', {"request": request})

@app.post('/select_songs')
async def select_songs(request: Request):
    # Retrieve selected songs from the client
    data = await request.json()
    selected_songs = data.get('songs', [])

    # Save selected songs to the CSV file
    with CSV_FILE.open('a', newline='') as file:
        writer = csv.writer(file)
        for song in selected_songs:
            writer.writerow([song['title'], song['artist']])

    return JSONResponse({
        'status': 'success',
        'selected_songs': selected_songs
    })

# Mount static files for serving JS or CSS if needed
app.mount("/", StaticFiles(directory=CLIENT_FOLDER), name="static")

