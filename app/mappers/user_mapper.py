from app.database.db import User
from app.models.user_dto import UserDto


def userdto_to_user(dto:UserDto):
    return User(
        name=dto.name,
        gender=dto.gender,
        email=dto.email,
        age=dto.age,
        is_salon_owner=dto.is_salon_owner,
        hashed_password=dto.password

    )

def user_to_userdto(user:User):
    return UserDto(
        name=user.name,
        gender=user.gender,
        email=user.email,
        age=user.age,
        is_salon_owner=user.is_salon_owner,
        password=user.hashed_password
    )