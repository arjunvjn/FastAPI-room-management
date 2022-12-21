from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db_setup import Base

class RoomDetails(Base):
    __tablename__ = 'room_details'
    id = Column(Integer, primary_key=True)
    room_price = Column(Float, nullable=False)
    room_type = Column(String(100), nullable=False)
    hotel_name = Column(String(200), nullable=False)
    no_of_rooms = Column(Integer, default=50)
    booked_user = relationship('RoomBooking', back_populates='room_info')