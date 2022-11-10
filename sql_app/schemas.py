from typing import List, Union
from pydantic import BaseModel

#-- Request Vehicle --#
class RequestVehicle(BaseModel):
    Id: int
    Militar: str
    Sec: str
    ChefeViatura: str
    TipoViatura: str
    QtdPassageiros: str
    DataSaida: str
    Local: str
    Obs: str
    Destino: str
    DataRetorno: str
    Status: str

    class Config:
        orm_mode = True

class RequestVehicleStatus(BaseModel):
    Id: int
    Status: str

    class Config:
        orm_mode = True

#-- Vehicle --#
class Vehicle(BaseModel):
    Id: int
    Placa: str
    Modelo: str
    QtdPassageiros: str
    Status: str

    class Config:
        orm_mode = True

class VehicleId(BaseModel):
    Id: int

    class Config:
        orm_mode = True

class VehicleStatus(BaseModel):
    Id: int
    Status: str

    class Config:
        orm_mode = True

#-- User --#
class User(BaseModel):
    Id: int
    Username: str
    Password: str
    Name: str
    CPF: str
    Role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str

class Login(BaseModel):
    Username: str
    Password: str

class SignUpUser(BaseModel):
    Username: str
    Password: str
    Name: str
    CPF: str
    Role: str

    class Config:
        orm_mode = True