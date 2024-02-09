from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import jwt
from app.database.db import get_db, User
from app.mappers.user_mapper import userdto_to_user
from app.models.login import Login
from app.models.response_dto import ResponseDto
from app.models.user_dto import UserDto

# db_session = get_db()
db = get_db()


def get_all_users():
    try:
        result = db.query(User).all()
    except Exception as e:
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "Successfully fetched all users", "data": result}


def save_user(dto: UserDto):
    user = userdto_to_user(dto)
    user.set_password(user.hashed_password)
    try:
        db.add(user)
        db.commit()
        jwt_token = jwt.generate_jwt(
         db.query(User).filter_by(email=dto.email).first()
        )

    except Exception as e:
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User created successfully", "data": {"token": jwt_token, "user":user}}


def get_user(email: str):
    try:
        user = db.query(User).filter_by(email=email).first()
    except Exception as e:
        return {"status": 500, "message": e}
    else:
        return ResponseDto(status=200, message="User Fetched successfully", data=user)

def update_user(dto: UserDto):
    try:
        user = db.query(User).filter_by(email=dto.email).first()
        user.name = dto.name
        user.gender = dto.gender
        user.age = dto.age
        user.is_salon_owner = True if dto.is_salon_owner else False
        user.set_password(dto.password)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User Updated successfully"}


def delete_user(dto: UserDto):
    try:
        user = db.query(User).filter_by(email=dto.email).first()
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User deleted successfully"}


def login_user(login: Login):
    try:
        user = db.query(User).filter_by(email=login.email).first()
        jwt_token = ""
        if user.check_password(login.password):
            jwt_token = jwt.generate_jwt(user)
        else:
            raise HTTPException(status_code=400, detail="Invalid Username Or Password")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Username Or Password")
    else:
        return {"status": 200, "message": "Successfully logged in", "data": {"token": jwt_token, "user":user}}
