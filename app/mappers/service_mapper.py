from sqlalchemy.orm import Session

from app.database.db import Service
from app.mappers.salon_mapper import salon_dto_mapper, salon_mapper
from app.models.service_dto import ServiceDto


def map_service_to_dto(service: Service) -> ServiceDto:
    return ServiceDto(
        id=service.id,
        name=service.name,
        description=service.description,
        price=service.price,
        img_1=service.img_1,
        img_2=service.img_2,
        img_3=service.img_3,
        img_4=service.img_4,
        img_5=service.img_5,
        slot_count=service.slot_count,
        salon_id=service.salon_id,
        salon=salon_dto_mapper(service.salon) if service.salon else None
    )

def map_dto_to_service(dto: ServiceDto) -> Service:
    return Service(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        price=dto.price,
        img_1=dto.img_1,
        img_2=dto.img_2,
        img_3=dto.img_3,
        img_4=dto.img_4,
        img_5=dto.img_5,
        slot_count=dto.slot_count,
        salon_id=dto.salon_id,
        salon=salon_mapper(dto.salon) if dto.salon else None
    )
