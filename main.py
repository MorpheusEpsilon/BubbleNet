from fastapi import FastAPI
from ai_integration import router as ai_router  # Import the ai router
from control import router as control_router  # Import the control router
app = FastAPI()

app.include_router(ai_router)  # Register the router

@app.get("/")
def read_root():
    return {"message": "Hello World"}