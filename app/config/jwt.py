from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer

import jwt
from app.database.db import User
from app.models.user_dto import UserDto

# Secret key for signing (keep this secure!)
secret_key = "n5o54_m5-Y54a954a954a_54a954a954a954a954a954a954a954a9"

def generate_jwt(user: User):
    # Generate the JWT

    payload ={
        "id": user.id,
        "email": user.email,
        "gender": user.gender,
        "age": user.age,
        "name": user.name,
        "password":user.hashed_password
    }

    encoded_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
    print(encoded_jwt)  # Output: eyJ0eXAiO... (example token)
    return encoded_jwt


def decode_jwt(encoded_jwt):
     # Decode the token using the same secret key
    decoded_payload = jwt.decode(encoded_jwt, secret_key, algorithms=["HS256"])
    print(decoded_payload)  # Output: {'user_id': 123, 'username': 'johndoe', 'email': 'johndoe@example.com'}
    return decoded_payload


# OAuth2PasswordBearer for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        print(payload)
        user = UserDto(**payload)
        return user
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception



