from fastapi import APIRouter
from fastapi import Depends, Request, HTTPException
from sql_app.database import SessionLocal, engine, get_db
from sql_app import crud
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/pages")

templates = Jinja2Templates(directory="Templates")

@router.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/sigin/vehicles", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("cadastro_vtr.html", {"request": request})

@router.get("/request/vehicles", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("pedido_vtr.html", {"request": request})

@router.get("/solicitations", response_class=HTMLResponse)
async def view_solicitations(request: Request, db: Session = Depends(get_db)):
    solicitations = crud.get_all_request_vehicle(db)
    return templates.TemplateResponse("vehicle_solicitations.html", {"request": request, "solicitations": solicitations})

@router.get("/solicitation/details/{id}", response_class=HTMLResponse)
async def view_solicitation_details(id: int, request: Request, db: Session = Depends(get_db)):
    solicitation = crud.get_request_vehicle(db, id)
    return templates.TemplateResponse("vehicle_solicitation_details.html", {"request": request, "solicitation": solicitation})