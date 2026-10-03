from fastapi import FastAPI

from app.routers.auth import router as auth_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)