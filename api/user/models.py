from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_setup import Base

class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False)
    booked_room = relationship('RoomBooking', back_populates='user_info')