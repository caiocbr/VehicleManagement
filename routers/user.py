from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, Request, HTTPException, status, Response, Request
from sql_app.database import SessionLocal, engine, get_db
from sql_app import crud
from sqlalchemy.orm import Session
from sql_app import schemas
import auth_functions
from datetime import timedelta

router = APIRouter(prefix="/user")

# Fazer Login
@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(response: Response, login: schemas.Login, db: Session = Depends(get_db)):
    user = auth_functions.authenticate_user(db, login.Username, login.Password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_functions.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_functions.create_access_token(
        data={"sub": user.Username}, expires_delta=access_token_expires
    )
    
    response.set_cookie('access_token', access_token, auth_functions.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        auth_functions.ACCESS_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, True, 'lax')

    return {"access_token": access_token}

# Fazer Cadastro
@router.post("/signup/", status_code=200)
def create_user(request: Request, userSign: schemas.SignUpUser, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    userSign = auth_functions.create_user(db, userSign)
    return userSign

# Delete User
@router.delete("/delete/", status_code=200)
def create_user(request: Request, userSign: schemas.DeleteUser, db: Session = Depends(get_db)):
    user = auth_functions.verify_user(db, request)
    if user == None or user.Role == "Regular":
        raise HTTPException(status_code=401)

    userSign = crud.delete_user(db, userSign.Username)