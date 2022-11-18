from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class RequestVehicle(Base):
    __tablename__ = "VehiclesRequest"

    Id = Column(Integer, primary_key=True, index=True)
    Militar = Column(String, nullable=False)
    Sec = Column(String, nullable=False)
    ChefeViatura = Column(String, nullable=False)
    Viatura = Column(String, nullable=False)
    QtdPassageiros = Column(String, nullable=False)
    DataSaida = Column(Date, nullable=False)
    HorarioSaida = Column(String, nullable=False)
    Local = Column(String, nullable=False)
    Obs = Column(String)
    Destino = Column(String, nullable=False)
    DataRetorno = Column(Date, nullable=False)
    Status = Column(String, nullable=False)
    HorarioRetorno = Column(String, nullable=False)
    Solicitante = Column(String, nullable=False)
    DataPedido = Column(DateTime, nullable=False)

class Vehicle(Base):
    __tablename__ = "Vehicles"

    Id = Column(Integer, primary_key=True, index=True)
    Placa = Column(String, nullable=False, unique=True)
    Modelo = Column(String, nullable=False)
    QtdPassageiros = Column(Integer, nullable=False)
    Status = Column(String, nullable=False)
    Tipo = Column(String, nullable=False)
    T4x4 = Column(String, nullable=False)
    Obs = Column(String)

class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, index=True)
    Username = Column(String, nullable=False, unique=True)
    Password = Column(String, nullable=False)
    Name = Column(String, nullable=False)
    CPF = Column(String, nullable=False, unique=True)
    Role = Column(String, nullable=False)