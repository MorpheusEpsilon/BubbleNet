from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# In-memory store for demo; replace with DB in production
site_controls = {}  # { "site_url": "blocked"/"allowed" }

@app.get("/control", response_class=HTMLResponse)
async def control_page(site: str):
    """Show a page with Allow and Block buttons"""
    return f"""
    <html>
        <body>
            <h2>Site Control</h2>
            <p>Do you want to allow or block <strong>{site}</strong>?</p>
            <form action="/control_action" method="post">
                <input type="hidden" name="site" value="{site}">
                <button type="submit" name="action" value="allow">Allow</button>
                <button type="submit" name="action" value="block">Block</button>
            </form>
        </body>
    </html>
    """

@app.post("/control_action", response_class=HTMLResponse)
async def control_action(site: str = Form(...), action: str = Form(...)):
    if action not in ["allow", "block"]:
        return HTMLResponse(f"Invalid action: {action}", status_code=400)

    site_controls[site] = action
    return f"""
    <html>
        <body>
            <h2>Site Control Updated</h2>
            <p>The site <strong>{site}</strong> is now <strong>{action}ed</strong>.</p>
        </body>
    </html>
    """