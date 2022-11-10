from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from fastapi import Depends

#-- Request Vehicle --#
def insert_request_vehicle(db: Session, request: schemas.RequestVehicle):
    db_request = models.RequestVehicle(
        Militar = request.Militar,
        Sec = request.Sec,
        ChefeViatura = request.ChefeViatura,
        TipoViatura = request.TipoViatura,
        QtdPassageiros = request.QtdPassageiros,
        DataSaida = request.DataSaida,
        Local = request.Local,
        Obs = request.Obs,
        Destino = request.Destino,
        DataRetorno = request.DataRetorno,
        Status = "Pendente"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_all_request_vehicle(db: Session):
    return db.query(models.RequestVehicle).all()

def delete_request_vehicle(db: Session, id: int):
    return db.query(models.RequestVehicle).filter(models.RequestVehicle.Id == id).delete()

def change_status_request_vehicle(db: Session, id: int, status: str):
    vehicle = db.query(models.RequestVehicle).filter(models.RequestVehicle.Id == id)
    vehicle.update({"Status": status})
    db.commit()

#-- Vehicle --#
def insert_vehicle(db: Session, vehicle: schemas.Vehicle):
    db_vehicle = models.Vehicle(
        Placa = vehicle.Placa,
        Modelo = vehicle.Modelo,
        QtdPassageiros = vehicle.QtdPassageiros,
        Status = "Livre"
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_all_vehicle(db: Session):
    return db.query(models.Vehicle).all()

def delete_vehicle(db: Session, id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.Id == id).delete()

def change_status_vehicle(db: Session, id: int, status: str):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.Id == id)
    vehicle.update({"Status": status})
    db.commit()
