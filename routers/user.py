from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, Request, HTTPException, status, Response
from sql_app.database import SessionLocal, engine, get_db
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

# Pegar Usuário
@router.get("/me/", response_model=schemas.User)
def read_user_me(request: Request, db: Session = Depends(get_db)):
    current_user = auth_functions.verify_user(db, request, "Regular")
    return current_user

# Fazer Cadastro
@router.post("/signup/", status_code=200)
def create_user(user: schemas.SignUpUser, db: Session = Depends(get_db)):
    user = auth_functions.create_user(db, user)
    return user