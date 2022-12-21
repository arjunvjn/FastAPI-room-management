from sqlalchemy.orm import Session
from pydantic import BaseModel
from db_setup import engine
from typing_extensions import Literal
from typing import Union
from fastapi import APIRouter, Depends
from auth.auth_bearer import JWTBearer
from .models import RoomDetails
from user_permission import is_user_staff

RoomType = Union[
    Literal['Single'],
    Literal['Double'],
    Literal['Family']
]

class Room(BaseModel):
    room_price : float
    room_type : RoomType
    hotel_name : str
    no_of_rooms : int

router = APIRouter()

@router.get('/room_list/', tags=['Room'])
async def get_room_list():
    session = Session(bind=engine, expire_on_commit=False)
    room_list = session.query(RoomDetails).all()
    session.close()
    return room_list

@router.post('/add_room_details/', dependencies=[Depends(JWTBearer())], tags=['Room'])
async def create_room(room_details : Room, token : str = Depends(JWTBearer())):
    if is_user_staff(token):
        try:
            room = RoomDetails(room_price=room_details.room_price, room_type=room_details.room_type, hotel_name=room_details.hotel_name, no_of_rooms=room_details.no_of_rooms)
            session = Session(bind=engine, expire_on_commit=False)
            session.add(room)
            session.commit()
            session.close()
            return 'Entered room details into database'
        except:
            return 'Error'
    else:
        return 'Authentication Failed'

@router.put('/update_room_details/{room_id}', dependencies=[Depends(JWTBearer())], tags=['Room'])
async def update_room(room_details : Room, room_id : int, token : str = Depends(JWTBearer())):
    if is_user_staff(token):
        session = Session(bind=engine, expire_on_commit=False)
        try:
            room  = session.query(RoomDetails).get(room_id)
            if room:
                room.room_price = room_details.room_price
                room.room_type = room_details.room_type
                room.hotel_name = room_details.hotel_name
                room.no_of_rooms=room_details.no_of_rooms
                session.commit()
                msg = 'Room details updated'
            else:
                msg = f'Room with id {room_id} is not here'
        except:
            msg = 'Error'
        session.close()
        return msg
    else:
        return 'Authentication Failed'

@router.delete('/delete_room/{room_id}', dependencies=[Depends(JWTBearer())], tags=['Room'])
async def delete_room(room_id : int, token : str = Depends(JWTBearer())):
    if is_user_staff(token):
        session = Session(bind=engine, expire_on_commit=False)
        try:
            room  = session.query(RoomDetails).get(room_id)
            if room:
                session.delete(room)
                session.commit()
                msg = 'Room details deleted'
            else:
                msg = f'Room with id {room_id} is not here'
        except:
            msg = 'Error'
        session.close()
        return msg
    else:
        return 'Authentication Failed'