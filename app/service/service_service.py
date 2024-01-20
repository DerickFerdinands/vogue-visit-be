from app.database.db import get_db, Salon, Service
from app.mappers.service_mapper import map_dto_to_service
from app.models.salon_dto import SalonDto
from app.models.service_dto import ServiceDto
from app.models.user_dto import UserDto

# db_session = get_db()
db = get_db()


def get_all_services():
    try:
        print("Getting all Services...")
        result = db.query(Service).all()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        # result.foreach()
        return {"status": 200, "message": "Successfully fetched all services", "data": result}


def save_service(serviceDto: ServiceDto, user: UserDto):
    try:
        service = map_dto_to_service(serviceDto)
        print('1', service)
        salon = db.query(Salon).filter_by(owner_id=user.id).first()
        print('2', salon)
        service.salon = salon
        print('3')
        db.add(service)
        print('4')
        db.commit()
        print(5)
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "Salon created successfully"}


def get_service(id: int):
    try:
        service = db.query(Service).filter_by(id=id).first()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "salon Fetched successfully", "data": service}


def update_service(dto: ServiceDto, user: UserDto):
    try:

        # Find the service in the salon's services
        service = db.query(Service).filter_by(id=dto.id).first()

        if service:
            # Update service attributes using ServiceDto
            service.name = dto.name
            service.description = dto.description
            service.price = dto.price
            service.img_1 = dto.img_1
            service.img_2 = dto.img_2
            service.img_3 = dto.img_3
            service.img_4 = dto.img_4
            service.img_5 = dto.img_5
            service.slot_count = dto.slot_count
            db.commit()
            return {"status": 200, "message": "Salon updated successfully"}
        else:
            return {"status": 404, "message": "Salon not found"}
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": str(e)}


def delete_service(dto: ServiceDto,user: UserDto):
    try:
        salon = db.query(Service).filter_by(id=dto.id).first()
        db.delete(salon)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User deleted successfully"}
