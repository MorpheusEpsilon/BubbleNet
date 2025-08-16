from fastapi import FastAPI
from ai_integration import router  # Import the router

app = FastAPI()

app.include_router(router)  # Register the router

@app.get("/")
def read_root():
    return {"message": "Hello World"}