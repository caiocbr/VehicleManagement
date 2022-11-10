from datetime import datetime, timedelta
from typing import Union, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from sql_app import models, schemas
from fastapi import Depends, FastAPI, HTTPException, status, Request
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session

SECRET_KEY = "c9016987f9e3f17a15782632d908a0ba137d5565d718a6970c9830c7b8a82451"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.Username == username).first()
    return user

def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        Username = user.Username,
        Password = pwd_context.hash(user.Password),
        Name = user.Name,
        CPF = user.CPF,
        Role = user.Role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.Password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_user(db: Session, request: Request, role: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.cookies.get("access_token")
        if token is None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None or user.Role != role:
        raise credentials_exception
    return user