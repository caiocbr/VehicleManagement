from typing import Union, List
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi import Depends, Request, HTTPException, status, Response, Request
from sql_app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sql_app import schemas, crud
from datetime import timedelta
import auth_functions

router = APIRouter(prefix="/solicitation")

# Pedido de veículo
@router.post("/", status_code=200)
def solicitation_vehicle(request: Request, requestVehicle: schemas.RequestVehicleForm = Depends(), db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        raise HTTPException(status_code=401)

    db_request = crud.insert_request_vehicle(db, requestVehicle)
    if db_request == None:
        raise HTTPException(status_code=500)

# Consulta de pedido
@router.get("/", response_model=List[schemas.RequestVehicle])
def get_vehicles(request: Request, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        raise HTTPException(status_code=401)

    requestsVehicle = crud.get_all_request_vehicle(db)
    return requestsVehicle

# Solucionar pedido
@router.post("/resolution")
def resolve_solicitation(request: Request, solicitaion: schemas.RequestVehicleStatus, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None:
        raise HTTPException(status_code=401)

    crud.change_status_request_vehicle(db, solicitaion.Id, solicitaion.Status)
