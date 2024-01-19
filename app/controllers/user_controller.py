from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db, User
from app.mappers.user_mapper import userdto_to_user
from app.models.login import Login
from app.models.user_dto import UserDto
from app.service.user_service import save_user, get_all_users, update_user, delete_user, login_user, get_user

user_router = APIRouter(prefix="/users")

@user_router.get("/all")
async def fetch_users():
    return get_all_users()

@user_router.get("/{email}")
async def fetch_user(email:str):
    return get_user(email)

@user_router.post("/", response_model=None)
async def create_user(user: UserDto):
    return save_user(user)

@user_router.put("/", response_model=None)
async def create_user(user: UserDto):
    return update_user(user)

@user_router.delete("/", response_model=None)
async def remove_user(user: UserDto):
    return delete_user(user)

@user_router.post("/login", response_model=None)
async def login(login: Login):
    return login_user(login)

