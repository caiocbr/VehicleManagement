from typing import Union, List
from fastapi import APIRouter, Form, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sql_app.database import SessionLocal, engine, get_db
from sql_app import crud, schemas
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import auth_functions
from datetime import datetime, timedelta, date

router = APIRouter(prefix="/pages")

templates = Jinja2Templates(directory="Templates")

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, result: str = ""):
    return templates.TemplateResponse("login.html", {"request": request, "result": result})

@router.post("/login", response_class=HTMLResponse)
async def authentication(request: Request, response: Response, username: Union[str, None] = Form(None), password: Union[str, None] = Form(None), db: Session = Depends(get_db)):
    if username == None or password == None:
         return templates.TemplateResponse("login.html", {"request": request, "result": ""})
    
    user = auth_functions.authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "result": "Usuário ou senha inválidos"})

    access_token_expires = timedelta(minutes=auth_functions.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_functions.create_access_token(
        data={"sub": user.Username}, expires_delta=access_token_expires
    )
    
    response.set_cookie('access_token', access_token, auth_functions.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        auth_functions.ACCESS_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, True, 'lax')

    response = RedirectResponse("http://localhost:8000/pages/home", status_code=303)
    response.set_cookie(key="access_token", value=access_token)
    return response

@router.get("/logout", response_class=HTMLResponse)
async def logout(response: Response):
    response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
    response.delete_cookie("access_token")
    return response

@router.get("/signup/vehicles", response_class=HTMLResponse)
async def signup_vehicles(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    return templates.TemplateResponse("cadastro_vtr.html", {"request": request, "result": ""})

@router.post("/signup/vehicles", response_class=HTMLResponse)
async def signup_vehicles_bd(request: Request, requestVehicle: schemas.VehicleForm = Depends(), db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    vehicle = crud.insert_vehicle(db, requestVehicle)
    if vehicle == None:
        return templates.TemplateResponse("cadastro_vtr.html", {"request": requestVehicle, "result": "Erro no cadastro de veículo!"})
    
    response = RedirectResponse("http://localhost:8000/pages/vehicles", status_code=303)
    response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
    return response

@router.get("/solicitation", response_class=HTMLResponse)
async def request_vehicles(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    return templates.TemplateResponse("pedido_vtr.html", {"request": request})

@router.post("/solicitation", status_code=200)
def solicitation_vehicle(request: Request, requestVehicle: schemas.RequestVehicleForm = Depends(), db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response
        
    crud.insert_request_vehicle(db, requestVehicle, user.Username)

    response = RedirectResponse("http://localhost:8000/pages/solicitations", status_code=303)
    response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
    return response

@router.get("/solicitations", response_class=HTMLResponse)
async def view_solicitations(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    if user.Role == "Regular":
        solicitations = crud.get_solicitations_by_user(db, user.Username)
    else:
        solicitations = crud.get_all_request_vehicle(db)
    
    return templates.TemplateResponse("vehicle_solicitations.html", {"request": request, "solicitations": solicitations})

@router.get("/solicitation/details/{id}", response_class=HTMLResponse)
async def view_solicitation_details(id: int, request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    solicitation = crud.get_request_vehicle(db, id)

    if solicitation.DataRetorno > date.today():
        role = "Regular"
    else:
        role = user.Role

    return templates.TemplateResponse("vehicle_solicitation_details.html", {"request": request, "solicitation": solicitation, "role": role})

@router.post("/solicitation/details/{id}/{status}", response_class=HTMLResponse)
async def view_solicitation_details(id: int, status: str, request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    crud.change_status_request_vehicle(db, id, status)
    response = RedirectResponse("http://localhost:8000/pages/solicitations", status_code=303)
    response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
    return response

@router.get("/vehicles", response_class=HTMLResponse)
async def show_vehicles(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    vehicles = crud.get_all_vehicle(db)
    return templates.TemplateResponse("vehicles.html", {"request": request, "vehicles": vehicles})

@router.get("/vehicle/details/{placa}", response_class=HTMLResponse)
async def show_vehicle_details(request: Request, placa: str, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    vehicle = crud.get_vehicle_by_plaque(db, placa)
    return templates.TemplateResponse("vehicle_details.html", {"request": request, "vehicle": vehicle})

@router.post("/vehicle/details/{placa}", response_class=HTMLResponse)
async def change_status_vehicle(request: Request, placa: str, status: schemas.VehicleStatusForm = Depends(), db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        response = RedirectResponse("http://localhost:8000/pages/login", status_code=303)
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
        return response

    vehicle = crud.get_vehicle_by_plaque(db, placa)
    crud.change_status_vehicle(db, vehicle.Id, status.Status)

    response = RedirectResponse("http://localhost:8000/pages/vehicles", status_code=303)
    response.set_cookie(key="access_token", value=request.cookies.get("access_token"))
    return response