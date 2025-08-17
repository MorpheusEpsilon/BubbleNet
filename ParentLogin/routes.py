from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Templates are in ParentLogin/Templates
templates = Jinja2Templates(directory="ParentLogin/Templates")

# Hardcoded credentials (replace with DB later)
PARENT_USERNAME = "parent"
PARENT_PASSWORD = "bubble123"

# GET: Show login page at /parent-login
@router.get("/parent-login", response_class=HTMLResponse)
async def parent_login_get(request: Request, error: str = None):
    return templates.TemplateResponse(
        "parent_login.html",
        {"request": request, "error": error}
    )

# POST: Handle login form submission
@router.post("/parent/login", response_class=HTMLResponse)
async def parent_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == PARENT_USERNAME and password == PARENT_PASSWORD:
        # Redirect to control page after successful login
        return RedirectResponse(url="/control?site=", status_code=303)
    else:
        return templates.TemplateResponse(
            "parent_login.html",
            {"request": request, "error": "Invalid username or password"},
            status_code=401
        )
