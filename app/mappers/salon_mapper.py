from app.database.db import User, Salon
from app.models.salon_dto import SalonDto
from app.models.user_dto import UserDto


from sqlalchemy.orm import Session

def salon_dto_mapper(salon: Salon) -> SalonDto:
    return SalonDto(
        id=salon.id,
        name=salon.name,
        description=salon.description,
        location=salon.location,
        owner_id=salon.owner_id,
        salon_owner=salon.salon_owner,
        instagram_url=salon.instagram_url,
        facebook_url=salon.facebook_url,
        phone_num=salon.phone_num,
        email=salon.email,
        img_1=salon.img_1,
        img_2=salon.img_2,
        img_3=salon.img_3,
        img_4=salon.img_4,
        img_5=salon.img_5
    )

def salon_mapper(salon_dto: SalonDto) -> Salon:
    return Salon(
        id=salon_dto.id,
        name=salon_dto.name,
        description=salon_dto.description,
        location=salon_dto.location,
        owner_id=salon_dto.owner_id,
        salon_owner=salon_dto.salon_owner,
        instagram_url=salon_dto.instagram_url,
        facebook_url=salon_dto.facebook_url,
        phone_num=salon_dto.phone_num,
        email=salon_dto.email,
        img_1=salon_dto.img_1,
        img_2=salon_dto.img_2,
        img_3=salon_dto.img_3,
        img_4=salon_dto.img_4,
        img_5=salon_dto.img_5
    )
