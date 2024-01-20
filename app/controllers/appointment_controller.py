from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.jwt import get_current_user
from app.database.db import get_db, User
from app.mappers.user_mapper import userdto_to_user
from app.models.appointment_rq import AppointmentRQ
from app.models.login import Login
from app.models.user_dto import UserDto
from app.service.appointment_service import get_all_appointments, save_appointment
from app.service.user_service import save_user, get_all_users, update_user, delete_user, login_user, get_user

appointment_router = APIRouter(prefix="/appointments")

@appointment_router.get("/all")
async def fetch_appointments():
    return get_all_appointments()

@appointment_router.get("/{email}")
async def fetch_user(email:str):
    return get_user(email)

@appointment_router.post("/", response_model=None)
async def create_user(rq: AppointmentRQ, current_user: UserDto = Depends(get_current_user)):
    return save_appointment(rq, current_user)

@appointment_router.put("/", response_model=None)
async def create_user(user: UserDto):
    return update_user(user)

@appointment_router.delete("/", response_model=None)
async def remove_user(user: UserDto):
    return delete_user(user)

@appointment_router.post("/login", response_model=None)
async def login(login: Login):
    return login_user(login)

