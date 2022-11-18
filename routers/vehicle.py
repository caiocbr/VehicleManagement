from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, Request, HTTPException, status, Response
from sql_app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sql_app import schemas, crud
import aux_functions
from datetime import date, datetime
import auth_functions

router = APIRouter(prefix="/vehicle")

# Cadastro Viatura
@router.post("/signup", status_code=200)
def signup_vehicle(request: Request, vehicle: schemas.Vehicle, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    db_request = crud.insert_vehicle(db, vehicle)
    if db_request == None:
        raise HTTPException(status_code=500)

# Deletar Viatura
@router.delete("/delete", status_code=200)
def delete_vehicle(request: Request, id: schemas.VehicleId, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    crud.delete_vehicle(db, id.Id)

# Pegar todas as viatura
@router.get("/query", response_model=List[schemas.Vehicle])
def get_all_vehicle(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    return crud.get_all_vehicle(db)

# Consultar Viatura
@router.post("/query", response_model=List[schemas.Vehicle])
def get_vehicle(request: Request, data: schemas.RequestDate, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    vehicles = crud.get_all_active_vehicle(db)
    response = []

    if ((data.DataSaida - date.today()).days == 1 and datetime.now().strftime('%H:%M') > "14:00") or (data.DataSaida - date.today()).days < 1:
        return response

    for vehicle in vehicles:
        if vehicle.Tipo == data.TipoViatura and int(vehicle.QtdPassageiros) >= data.QtdPassageiros:
            vehicleSolicitations = crud.get_active_requests_by_vehicle_id(db, vehicle.Modelo + " " + vehicle.Placa)
            validated = True
            
            for solicitation in vehicleSolicitations:
                if not aux_functions.check_interval(data.DataSaida, data.HorarioSaida, data.DataRetorno, data.HorarioRetorno, solicitation):
                    validated = False
            
            if validated:    
                response.append(vehicle)

    return response

# Alterar Status Viatura
@router.post("/status")
def change_status_vehicle(request: Request, vehicle: schemas.VehicleStatus, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    crud.change_status_vehicle(db, vehicle.Id, vehicle.Status)