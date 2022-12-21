from operator import or_
from sqlalchemy.orm import Session
from api.user.models import UserDetails
from pydantic import BaseModel
from db_setup import engine
from fastapi import APIRouter, Depends
from .models import RoomBooking
from api.room.models import RoomDetails
from datetime import date
from auth.auth_bearer import JWTBearer
from user_permission import is_user, is_user_staff

class BookRoom(BaseModel):
    start_date : date
    end_date : date

router = APIRouter()

@router.post('/book_room/{room_id}/', dependencies=[Depends(JWTBearer())], tags=['Book Room'])
def book_room(room_id : int, book_details : BookRoom, token : str = Depends(JWTBearer())):
    username : str = is_user(token)
    session = Session(bind=engine, expire_on_commit=False)
    user = session.query(UserDetails).filter(UserDetails.username==username).first()
    if user:
        try:
            room = session.query(RoomDetails).get(room_id)
            if room:
                check_room : int = session.query(RoomBooking).filter(RoomBooking.room==room_id).filter(or_(RoomBooking.start_date.between(book_details.start_date, book_details.end_date), RoomBooking.end_date.between(book_details.start_date, book_details.end_date))).count()
                if room.no_of_rooms-check_room > 0:
                    room_book = RoomBooking(user=user.id, room=room_id, start_date=book_details.start_date, end_date=book_details.end_date)
                    session.add(room_book)
                    session.commit()
                    msg = 'Room Booked'
                else:
                    msg = f'Room with id {room_id} is already booked'
            else:
                msg = f'Room with id {room_id} is not present'
        except:
            msg = 'Error'
    else:
        msg = 'Authentication Failed'
    session.close()
    return msg

@router.post('/room_available/', tags=['Book Room'])
def room_available(book_details : BookRoom):
    session = Session(bind=engine, expire_on_commit=False)
    rooms = session.query(RoomBooking).filter(or_(RoomBooking.start_date.between(book_details.start_date, book_details.end_date), RoomBooking.end_date.between(book_details.start_date, book_details.end_date))).all()
    booked_rooms : set = {room.room for room in rooms}
    room_list : list = [] 
    for room in session.query(RoomDetails).all():
        if room.id not in booked_rooms:
            room_list.append(room)
    return room_list

@router.get('/room_booking_details/', dependencies=[Depends(JWTBearer())], tags=['Book Room'])
def room_booking_details(token : str = Depends(JWTBearer())):
    if is_user_staff(token):
        session = Session(bind=engine, expire_on_commit=False)
        booked_room_details = []
        booked_room = session.query(RoomBooking).all()
        for booking in booked_room:
            details = {
                'Username' : booking.user_info.username,
                'Hotel Name' : booking.room_info.hotel_name,
                'Room Type' : booking.room_info.room_type,
                'From' : booking.start_date,
                'To' : booking.end_date,
                'Room Price' : booking.room_info.room_price
            }
            booked_room_details.append(details)
        session.close()
        return booked_room_details
    else:
        return 'Authentication Failed'

