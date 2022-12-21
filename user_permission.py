from auth.auth_handler import decodeJWT

def is_user_staff(token : str):
    user = decodeJWT(token)
    if user and user['role']=='staff':
        return True
    else:
        return False

def is_user(token : str):
    user = decodeJWT(token)
    if user and user['role']=='user':
        return user['username']
    else:
        return -1