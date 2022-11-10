from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routers import solicitation, user, vehicle

app = FastAPI()

templates = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/sigin/vehicles", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("cadastro_vtr.html", {"request": request})

@app.get("/request/vehicles", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("pedido_vtr.html", {"request": request})

app.include_router(user.router)
app.include_router(solicitation.router)
app.include_router(vehicle.router)
