from fastapi import FastAPI
from db_setup import Base, engine
from api.room import room_api
from api.user import user_api
from api.room_booking import room_book_api

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(room_api.router)
app.include_router(user_api.router)
app.include_router(room_book_api.router)