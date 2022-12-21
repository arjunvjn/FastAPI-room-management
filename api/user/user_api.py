from sqlalchemy.orm import Session
from pydantic import BaseModel
from db_setup import engine
from typing_extensions import Literal
from typing import Union
from fastapi import APIRouter
from .models import UserDetails
from passlib.context import CryptContext
from auth.auth_handler import signJWT

UserRole = Union[
    Literal['user'],
    Literal['staff']
]

class User(BaseModel):
    username : str
    password : str
    role : UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post('/user_registration/', tags=['User'])
async def create_user(user_details : User):
    global pwd_context
    session = Session(bind=engine, expire_on_commit=False)
    try:
        hashed_password = pwd_context.hash(user_details.password)
        user = UserDetails(username=user_details.username, password=hashed_password, role=user_details.role)
        session.add(user)
        session.commit()
        msg = 'Entered user details into database'
    except:
        if session.query(UserDetails).filter(UserDetails.username==user_details.username).exists():
            msg = 'User with this username already exist'
        else:
            msg = 'Error'
    session.close()
    return msg

@router.post('/user_login/', tags=['User'])
async def user_login(username : str, password : str):
    global pwd_context
    session = Session(bind=engine, expire_on_commit=False)
    try:
        user = session.query(UserDetails).filter(UserDetails.username==username).first()
        if pwd_context.verify(password, user.password):
            msg = signJWT(user)
        else:
            msg = 'Invalid Credentials'
    except:
        msg = 'Invalid Credentials'
    session.close()
    return msg