import time
from typing import Dict
import jwt
from pydantic import BaseModel
from typing_extensions import Literal
from typing import Union

JWT_SECRET = 'arjun'
JWT_ALGORITHM = 'HS256'

UserRole = Union[
    Literal['user'],
    Literal['staff']
]

class User(BaseModel):
    username : str
    password : str
    role : UserRole

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user: User) -> Dict[str, str]:
    payload = {
        "username": user.username,
        "role": user.role,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}