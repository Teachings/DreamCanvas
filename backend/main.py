import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router as api_router

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="ui"), name="static")

# Include all API routes
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
