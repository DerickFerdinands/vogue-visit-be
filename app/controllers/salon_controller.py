import jwt
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from starlette import status

from app.config.jwt import decode_jwt, get_current_user
from app.database.db import User
from app.models.user_dto import UserDto
from app.service.salon_service import *
from app.utils.aws_s3 import upload_to_s3, generate_s3_url

salon_router = APIRouter(prefix="/salons")





@salon_router.post("/upload")
async def upload_file(file: UploadFile = File(...), data: str = Form(...)):
    file_name = file.filename
    print(data)
    # Upload the file to S3
    if upload_to_s3(file.file, file_name):
        s3_url = generate_s3_url(file_name)
        return JSONResponse(content={"message": "File uploaded successfully", "data": data, "s3_url": s3_url})
    else:
        raise HTTPException(
            status_code=500,
            detail="Error uploading file. Please try again."
        )


@salon_router.get("/all")
async def fetch_salons():
    return get_all_salons()


@salon_router.get("/{email}")
async def fetch_salon(email: str):
    return get_salon(email)

@salon_router.post("/", response_model=None)
async def create_salon(salon: SalonDto, current_user: UserDto = Depends(get_current_user)):
    return save_salon(salon, current_user)


@salon_router.put("/", response_model=None)
async def modify_salon(salon: SalonDto, current_user: UserDto = Depends(get_current_user)):
    return update_salon(salon, current_user)


@salon_router.delete("/", response_model=None)
async def remove_salon(current_user: UserDto = Depends(get_current_user)):
    return delete_salon(current_user)
