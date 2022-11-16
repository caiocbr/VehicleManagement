from typing import List, Union
from pydantic import BaseModel
from fastapi import Form
import datetime

#-- Request Vehicle --#
class RequestVehicle(BaseModel):
    Id: int
    Militar: str
    Sec: str
    ChefeViatura: str
    Viatura: str
    QtdPassageiros: int
    DataSaida: datetime.date
    HorarioSaida: str
    Local: str
    Obs: str
    Destino: str
    DataRetorno: datetime.date
    HorarioRetorno: str
    Status: str
    Solicitante: str
    DataPedido: datetime.date

    class Config:
        orm_mode = True

class RequestVehicleForm:
    def __init__(
        self,
        Militar: str = Form(...),
        Sec: str = Form(...),
        ChefeViatura: str = Form(...),
        Viatura: str = Form(...),
        QtdPassageiros: int = Form(...),
        DataSaida: str = Form(...),
        HorarioSaida: str = Form(...),
        Local: str = Form(...),
        Obs: str = Form(...),
        Destino: str = Form(...),
        DataRetorno: str = Form(...),
        HorarioRetorno: str = Form(...)
    ):
        self.Militar = Militar
        self.Sec = Sec
        self.ChefeViatura = ChefeViatura
        self.Viatura = Viatura
        self.QtdPassageiros = QtdPassageiros
        self.DataSaida = DataSaida
        self.HorarioSaida = HorarioSaida
        self.Local = Local
        self.Obs = Obs
        self.Destino = Destino
        self.DataRetorno = DataRetorno
        self.HorarioRetorno = HorarioRetorno

class RequestDate(BaseModel):
    DataSaida: datetime.date
    HorarioSaida: str
    DataRetorno: datetime.date
    HorarioRetorno: str
    QtdPassageiros: int
    TipoViatura: str

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
    Tipo: str
    T4x4: str
    QtdPassageiros: int
    Obs: str
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

class VehicleForm:
    def __init__(
        self,
        Modelo: str = Form(...),
        Placa: str = Form(...),
        QtdPassageiros: int = Form(...),
        Tipo: str = Form(...),
        T4x4: str = Form(...),
        Obs: Union[str, None] = Form(...)
    ):
        self.Modelo = Modelo
        self.Placa = Placa
        self.QtdPassageiros = QtdPassageiros
        self.Tipo = Tipo
        self.T4x4 = T4x4
        self.Obs = Obs

class VehicleStatusForm:
    def __init__(
        self,
        Status: str = Form(...)
    ):
        self.Status = Status

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