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
from app.models.user_dto import UserDto
from app.service.salon_service import *
from app.service.service_service import get_all_services, get_service, save_service, update_service, delete_service, \
    get_services_by_owner_id, get_services_by_salon_id
from app.utils.aws_s3 import upload_to_s3, generate_s3_url

service_router = APIRouter(prefix="/services")

@service_router.get("/all")
async def fetch_services():
    return get_all_services()


@service_router.get("/id/{id}")
async def fetch_services(id: int):
    return get_service(id)

@service_router.get("/owner")
async def fetch_services_by_owner(current_user: UserDto = Depends(get_current_user)):
    return get_services_by_owner_id(current_user)

@service_router.get("/salon/{id}")
async def fetch_services_by_salon(id:int, current_user: UserDto = Depends(get_current_user)):
    return get_services_by_salon_id(id)

@service_router.post("/", response_model=None)
async def create_service(service: ServiceDto, current_user: UserDto = Depends(get_current_user)):
    return save_service(service, current_user)


@service_router.put("/", response_model=None)
async def modify_service(service: ServiceDto, current_user: UserDto = Depends(get_current_user)):
    return update_service(service, current_user)


@service_router.delete("/", response_model=None)
async def remove_service(service: ServiceDto, current_user: UserDto = Depends(get_current_user)):
    return delete_service(service, current_user)
