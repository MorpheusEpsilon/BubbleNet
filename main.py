from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from ai_integration import router as ai_router  # Import the ai router
from control import router as control_router  # Import the control router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing, allow all. Later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="ParentFrontEnd/static"), name="static")

templates = Jinja2Templates(directory="ParentFrontEnd/Templates")

app.include_router(ai_router)  # Register the router

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/check_url")
async def check_url(request: Request):
    body = await request.json()
    url = body.get("url", "").lower()

    # Dummy logic — expand blacklist
    blacklist = ["phishing", "malware", "kaotic"]
    if any(word in url for word in blacklist):
        return {"unsafe": True}
    return {"unsafe": False}

app.include_router(control_router)

from fastapi import APIRouter, Request

router = APIRouter()
