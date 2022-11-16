from typing import Union, List
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi import Depends, Request, HTTPException, status, Response
from sql_app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sql_app import schemas, crud
from datetime import timedelta

router = APIRouter(prefix="/solicitation")

# Pedido de veículo
@router.post("/", status_code=200)
def solicitation_vehicle(request: schemas.RequestVehicleForm = Depends(), db: Session = Depends(get_db)):
    db_request = crud.insert_request_vehicle(db, request)
    if db_request == None:
        return HTTPException(status_code=500)

# Consulta de pedido
@router.get("/", response_model=List[schemas.RequestVehicle])
def get_vehicles(db: Session = Depends(get_db)):
    requests = crud.get_all_request_vehicle(db)
    return requests

# Deletar pedido
@router.delete("/")
def delete_solicitation():
    pass

# Solucionar pedido
@router.post("/resolution")
def resolve_solicitation(solicitaion: schemas.RequestVehicleStatus, db: Session = Depends(get_db)):
    crud.change_status_request_vehicle(db, solicitaion.Id, solicitaion.Status)
