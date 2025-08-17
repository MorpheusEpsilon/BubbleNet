from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ParentLogin.routes import router as parent_router
from Backend.ai_integration import router as ai_router  # Import the ai router
from Backend.control import router as control_router  # Import the control router
from Backend.config import settings
from Dashboard.routes import router as dashboard_router



app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Static and templates
landing_templates = Jinja2Templates(directory="LandingPageFrontEnd")
app.mount("/landing-static", StaticFiles(directory="LandingPageFrontEnd/static"), name="landing-static")
app.mount("/parent-static", StaticFiles(directory="ParentLogin/static"), name="parent-static")


parent_templates = Jinja2Templates(directory="ParentFrontEnd/Templates")
app.mount("/static", StaticFiles(directory="ParentFrontEnd/static"), name="static")

app.mount("/dashboard-static", StaticFiles(directory="Dashboard/static"), name="dashboard-static")

#Routers
app.include_router(ai_router)  # Register the router
app.include_router(control_router)
app.include_router(parent_router)
app.include_router(dashboard_router)

@app.get("/", response_class=HTMLResponse)
async def read_landing(request: Request):
    return landing_templates.TemplateResponse("index.html", {"request": request})

#Handles the URL request
@app.post("/check_url")
async def check_url(request: Request):
    body = await request.json()
    url = body.get("url", "").lower()

    # Dummy logic - for early hard Blacklist
    return {"unsafe": any(word in url for word in settings.BLACKLIST)}
