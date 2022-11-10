from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, Request, HTTPException, status, Response
from sql_app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sql_app import schemas, crud
from datetime import timedelta

router = APIRouter(prefix="/vehicle")

# Cadastro viatura
@router.post("/vehicles/sigin", status_code=200)
def read_item(vehicle: schemas.Vehicle, db: Session = Depends(get_db)):
    db_request = crud.insert_vehicle(db, vehicle)
    if db_request == None:
        return HTTPException(status_code=500)

# Deletar viatura
@router.delete("/vehicles/delete", status_code=200)
def read_item(id: schemas.VehicleId, db: Session = Depends(get_db)):
    crud.delete_vehicle(db, id)

# Consulta viatura
@router.get("/vehicles/query", response_model=List[schemas.Vehicle])
def read_item(db: Session = Depends(get_db)):
    return crud.get_all_vehicle(db)

# Alterar status veiculo
@router.post("/vehicle/status")
def read_item(vehicle: schemas.VehicleStatus, db: Session = Depends(get_db)):
    crud.change_status_vehicle(db, vehicle.Id, vehicle.Status)