from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from . import storage

router = APIRouter()

# Templates folder
templates = Jinja2Templates(directory="ParentFrontEnd/Templates")

@router.get("/control", response_class=HTMLResponse)
async def control_page(request: Request, site: str):
    """
    Show page with Allow/Block buttons.
    Displays current status if already controlled.
    """
    # Check if site is currently in whitelist/blacklist
    if site in storage.get_whitelist():
        action = "allow"
    elif site in storage.get_blacklist():
        action = "block"
    else:
        action = None

    return templates.TemplateResponse(
        "control.html",
        {"request": request, "site": site, "action": action}
    )


#Handles the parent's page allow/block button
@router.post("/control_action", response_class=HTMLResponse)
async def control_action(request: Request, site: str = Form(...), action: str = Form(...)):
    """
    Update storage (whitelist/blacklist) and re-render the page.
    """
    if action not in ["allow", "block"]:
        return HTMLResponse(f"Invalid action: {action}", status_code=400)

    # Update storage lists
    if action == "allow":
        storage.add_to_whitelist(site)

        # remove from blacklist if it exists
        if site in storage.get_blacklist():
            bl = storage.get_blacklist()
            bl.remove(site)

            # Save updated blacklist
            storage._save_data({"whitelist": storage.get_whitelist(), "blacklist": bl})

    else:  # block
        storage.add_to_blacklist(site)

        # remove from whitelist if it exists
        if site in storage.get_whitelist():
            wl = storage.get_whitelist()
            wl.remove(site)
            # Save updated whitelist
            storage._save_data({"whitelist": wl, "blacklist": storage.get_blacklist()})

    return templates.TemplateResponse(
        "control.html",
        {"request": request, "site": site, "action": action}
    )
