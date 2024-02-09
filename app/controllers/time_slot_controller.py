import jwt
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from starlette import status

from app.config.jwt import decode_jwt, get_current_user
from app.database.db import User
from app.models.service_dto import ServiceDto
from app.models.time_slot_rq import TimeSlotRq
from app.models.user_dto import UserDto
from app.service.salon_service import *
from app.service.service_service import get_all_services, get_service, save_service, update_service, delete_service
from app.service.time_slot_service import get_all_slots, save_slots, get_slots_for_date, get_dates_and_slots, \
    get_dates_by_salon_id, get_slots_for_date_by_salon_id
from app.utils.aws_s3 import upload_to_s3, generate_s3_url

time_slot_router = APIRouter(prefix="/slots")

@time_slot_router.get("/all")
async def fetch_slots():
    return get_all_slots()


# @time_slot_router.get("/{email}")
# async def fetch_slot(email: int):
#     return get_service(email)

@time_slot_router.get("/date/{date}")
async def fetch_slot(date: str, current_user: UserDto = Depends(get_current_user)):
    return get_slots_for_date(date, current_user)

@time_slot_router.get("/salon/{salon_id}/date/{date}")
async def fetch_slot(salon_id:int, date: str, current_user: UserDto = Depends(get_current_user)):
    return get_slots_for_date_by_salon_id(salon_id, date)

@time_slot_router.get("/")
async def fetch_slot(current_user: UserDto = Depends(get_current_user)):
    return get_dates_and_slots(current_user)

@time_slot_router.get("/dates/salon/{salon_id}")
async def fetch_slot(salon_id:int, current_user: UserDto = Depends(get_current_user)):
    return get_dates_by_salon_id(salon_id)

@time_slot_router.post("/", response_model=None)
async def create_slots(slot_rq: TimeSlotRq, current_user: UserDto = Depends(get_current_user)):
    print(slot_rq)
    return save_slots(slot_rq, current_user)


# @time_slot_router.put("/", response_model=None)
# async def modify_slot(service: ServiceDto, current_user: UserDto = Depends(get_current_user)):
#     return update_service(service, current_user)
#
#
# @time_slot_router.delete("/", response_model=None)
# async def remove_slots(service: ServiceDto, current_user: UserDto = Depends(get_current_user)):
#     return delete_service(service, current_user)
