from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
from core.db import get_connection
from core.reg import register_submission

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    landpage = random.choice(["landpage1", "landpage2", "landpage3"])
    return templates.TemplateResponse(f"{landpage}/index.html", {"request": request, "landpage": landpage})

@app.post("/submit")
async def submit(request: Request, name: str = Form(...), email: str = Form(...), landpage: str = Form(...)):
    register_submission(landpage, name, email)
    return {"message": "Submission received"}
