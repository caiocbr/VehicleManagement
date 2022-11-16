from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, Request, HTTPException, status, Response
from sql_app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sql_app import schemas, crud
import aux_functions
from datetime import date, datetime

router = APIRouter(prefix="/vehicle")

# Cadastro Viatura
@router.post("/signup", status_code=200)
def read_item(vehicle: schemas.Vehicle, db: Session = Depends(get_db)):
    db_request = crud.insert_vehicle(db, vehicle)
    if db_request == None:
        return HTTPException(status_code=500)

# Deletar Viatura
@router.delete("/delete", status_code=200)
def read_item(id: schemas.VehicleId, db: Session = Depends(get_db)):
    crud.delete_vehicle(db, id)

# Pegar todas as viatura
@router.get("/query", response_model=List[schemas.Vehicle])
def read_item(db: Session = Depends(get_db)):
    return crud.get_all_vehicle(db)

# Consultar Viatura
@router.post("/query", response_model=List[schemas.Vehicle])
def read_item(data: schemas.RequestDate, db: Session = Depends(get_db)):
    vehicles = crud.get_all_active_vehicle(db)
    response = []

    if datetime.now().strftime('%H:%M') > "14:00" and (data.DataSaida - date.today()).days <= 1:
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
def read_item(vehicle: schemas.VehicleStatus, db: Session = Depends(get_db)):
    crud.change_status_vehicle(db, vehicle.Id, vehicle.Status)