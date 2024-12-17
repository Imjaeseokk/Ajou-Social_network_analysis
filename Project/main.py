from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import csv
from pathlib import Path
from fastapi.templating import Jinja2Templates
from recommendation_system import get_closest_song, df

app = FastAPI()

# Path to the Client folder where HTML files are located
BASE_DIR = Path(__file__).resolve().parent
CLIENT_FOLDER = BASE_DIR / "Client"
templates = Jinja2Templates(directory=CLIENT_FOLDER)

# Path to the CSV file where selected songs will be stored
CSV_FILE = BASE_DIR / "selected_songs.csv"

# Ensure the CSV file exists and has a header
if not CSV_FILE.exists():
    with CSV_FILE.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Artist'])

# Main Page: 노래 선택 페이지 렌더링
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# Result Page: 추천 결과 페이지 렌더링
@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

# 추천 로직 수행: 노래 제목을 기반으로 가장 유사한 노래 반환
@app.post("/recommend", response_class=JSONResponse)
async def recommend(title: str = Form(...)):
    try:
        closest_song = get_closest_song(df, title)
        return {
            "status": "success",
            "title": closest_song["Title"],
            "artist": closest_song.get("Artist", "Unknown"),
            "distance": closest_song["Distance"]
        }
    except ValueError as e:
        return {"status": "error", "message": str(e)}

# 노래 선택 결과 저장
@app.post("/save_selected", response_class=JSONResponse)
async def save_selected(title: str = Form(...), artist: str = Form(...)):
    try:
        # CSV 파일에 선택한 노래 저장
        with CSV_FILE.open('a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, artist])
        return {"status": "success", "message": f"Song '{title}' by {artist} saved successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Static 파일 서빙 (CSS, JS, 이미지 등)
app.mount("/static", StaticFiles(directory=CLIENT_FOLDER), name="static")
