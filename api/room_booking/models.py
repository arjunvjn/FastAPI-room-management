from email.policy import default
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from db_setup import Base

class RoomBooking(Base):
    __tablename__ = 'room_booking'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user_details.id'), nullable=False)
    user_info = relationship('UserDetails', back_populates='booked_room')
    room = Column(Integer, ForeignKey('room_details.id'), nullable=False)
    room_info = relationship('RoomDetails', back_populates='booked_user')  
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)