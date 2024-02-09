
from app.database.db import get_db, Salon, User
from app.mappers.salon_mapper import salon_mapper
from app.mappers.user_mapper import userdto_to_user
from app.models.login import Login
from app.models.salon_dto import SalonDto
from app.models.user_dto import UserDto
from app.service.user_service import get_user, update_user

# db_session = get_db()
db = get_db()


def get_all_salons():
    try:
        print("Getting all salons...")
        result = db.query(Salon).all()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        # result.foreach()
        return {"status": 200, "message": "Successfully fetched all salons", "data": result}


def save_salon(salon: SalonDto, user:UserDto):
    try:
        salon = salon_mapper(salon)
        salon_owner = db.query(User).filter_by(email=user.email).first()
        salon_owner.is_salon_owner = True
        salon.salon_owner = salon_owner
        db.add(salon)
        db.commit()

        retrieved_salon = db.query(Salon).filter_by(owner_id=user.id).first()
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "Salon created successfully", "data": retrieved_salon}


def get_salon(id:str):
    try:
        salon = db.query(Salon).filter_by(id=id).first()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "salon Fetched successfully", "data":salon}


def get_salon_by_id(user: UserDto):
    try:
        print("sjdgvfyuefvhbuyiwejks")
        print("User Id",user.id)
        salon = db.query(Salon).filter_by(owner_id=user.id).first()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "salon Fetched sefer successfully", "data":salon}


def update_salon( dto: SalonDto, user: UserDto):
    try:
        salon = db.query(Salon).filter_by(owner_id=user.id).first()
        if salon:
            # Update salon attributes using SalonDto
            salon.name = dto.name
            salon.description = dto.description
            salon.location = dto.location
            salon.instagram_url = dto.instagram_url
            salon.facebook_url = dto.facebook_url
            salon.phone_num = dto.phone_num
            salon.email = dto.email
            salon.img_1 = dto.img_1
            salon.img_2 = dto.img_2
            salon.img_3 = dto.img_3
            salon.img_4 = dto.img_4

            db.commit()
            return {"status": 200, "message": "Salon updated successfully"}
        else:
            return {"status": 404, "message": "Salon not found"}
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": str(e)}


def delete_salon(user: UserDto):
    try:
        salon = db.query(Salon).filter_by(owner_id=user.id).first()
        db.delete(salon)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User deleted successfully"}


