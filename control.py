from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/control")
def control_page(site: str):
    return HTMLResponse(content=f"""
        <html>
            <body>
                <h2>Manage Access for: {site}</h2>
                <form action="/control-action" method="post">
                    <input type="hidden" name="site" value="{site}">
                    <button name="action" value="allow">Allow</button>
                    <button name="action" value="timer">Set Timer</button>
                    <button name="action" value="block">Block</button>
                </form>
            </body>
        </html>
    """)

@router.post("/control-action")
def control_action(site: str = Form(...), action: str = Form(...)):
    # Save to DB or config
    print(f"Parent chose to {action} for {site}")
    return {"site": site, "action": action}
