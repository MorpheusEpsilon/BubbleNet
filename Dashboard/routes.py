#Route handling for the main page
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json, os

router = APIRouter(prefix="/dashboard")  # Prefix added
templates = Jinja2Templates(directory="Dashboard/templates")
STORAGE_FILE = "Backend/storage.json"

def read_storage():
    if not os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "w") as f:
            json.dump({"whitelist": [], "blacklist": []}, f)
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def write_storage(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# GET route for dashboard page
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = None):
    data = read_storage()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": username,
        "whitelist": data["whitelist"],
        "blacklist": data["blacklist"]
    })

# POST route to add site
@router.post("/add")
async def add_site(request: Request, site: str = Form(...), list_type: str = Form(...), username: str = Form(...)):
    data = read_storage()
    if list_type not in ["whitelist", "blacklist"]:
        list_type = "blacklist"

    if site and site not in data[list_type]:
        data[list_type].append(site)
        write_storage(data)

    return RedirectResponse(url=f"/dashboard?username={username}", status_code=303)

# POST route to remove site
@router.post("/remove")
async def remove_site(request: Request, site: str = Form(...), list_type: str = Form(...), username: str = Form(...)):
    data = read_storage()
    if list_type not in ["whitelist", "blacklist"]:
        list_type = "blacklist"

    if site in data[list_type]:
        data[list_type].remove(site)
        write_storage(data)

    return RedirectResponse(url=f"/dashboard?username={username}", status_code=303)
