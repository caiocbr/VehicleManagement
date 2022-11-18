from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routers import solicitation, user, vehicle, pages

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)
app.include_router(solicitation.router)
app.include_router(vehicle.router)
app.include_router(pages.router)