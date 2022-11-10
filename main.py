from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



# Autenticação
@app.post("/auth")
def read_root():
    pass

# Pedido de veículo
@app.post("/vehicle/request")
def read_item():
    pass

# Consulta de pedido
@app.get("/vehicle/request")
def read_item():
    pass

# Deletar pedido
@app.delete("/vehicle/request")
def read_item():
    pass

# Cadastro viatura
@app.get("/vehicles/sigin")
def read_item():
    pass

# Deletar viatura
@app.delete("/vehicles/delete")
def read_item():
    pass

# Consulta viatura
@app.get("/vehicles/query")
def read_item():
    pass

@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/sigin/vehicles", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("cadastro_vtr.html", {"request": request})

@app.get("/request/vehicles", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("pedido_vtr.html", {"request": request})

