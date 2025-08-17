from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

# Templates folder
templates = Jinja2Templates(directory="ParentFrontEnd/Templates")

# In-memory store (DB later)
site_controls = {}  # { "site_url": "allowed"/"blocked" }

@router.get("/control", response_class=HTMLResponse)
async def control_page(request: Request, site: str):
    """
    Show page with Allow/Block buttons.
    Displays current status if already controlled.
    """
    return templates.TemplateResponse(
        "control.html",
        {"request": request, "site": site, "action": site_controls.get(site)}
    )

@router.post("/control_action", response_class=HTMLResponse)
async def control_action(request: Request, site: str = Form(...), action: str = Form(...)):
    """
    Update site_controls and re-render the page.
    """
    if action not in ["allow", "block"]:
        return HTMLResponse(f"Invalid action: {action}", status_code=400)

    site_controls[site] = action
    return templates.TemplateResponse(
        "control.html",
        {"request": request, "site": site, "action": site_controls.get(site)}
    )
