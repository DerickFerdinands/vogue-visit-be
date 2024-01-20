from fastapi import HTTPException

from app.config import jwt
from app.database.db import get_db, User, Appointment, Service, TimeSlot
from app.models.appointment_rq import AppointmentRQ
from app.models.login import Login
from app.models.response_dto import ResponseDto
from app.models.user_dto import UserDto

# db_session = get_db()
db = get_db()


def get_all_appointments():
    try:
        result = db.query(Appointment).all()
    except Exception as e:
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "Successfully fetched all appointments", "data": result}


def save_appointment(rq: AppointmentRQ, dto: UserDto):
    try:

        service = db.query(Service).filter_by(id=rq.service_id).first()

        if not service.slot_count == len(rq.slots):
            raise HTTPException(status_code=404, detail="Invalid Appointment Slots")

        user = db.query(User).filter_by(id=dto.id).first()
        timeslots = []
        for slot in rq.slots:
            timeslt = db.query(TimeSlot).filter_by(id=slot).first()
            timeslt.is_booked = True
            timeslots.append(timeslt)
            appointment = Appointment(
                time_slot=timeslt,
                service=service,
                user=user,
                identifier=""+rq.slots[0]+user.id+service.id
            )

            db.add(appointment)

        # db.add(user)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "Appointment created successfully", "data":{
            "date": timeslots[0].date,
            "start_time": timeslots[0].start_time,
            "end_time": timeslots[len(timeslots)-1].end_time,
            "identifier": ""+rq.slots[0]+user.id+service.id

        }}


def get_user(email: str):
    try:
        user = db.query(User).filter_by(email=email).first()
    except Exception as e:
        return {"status": 500, "message": e}
    else:
        return ResponseDto(status=200, message="User Fetched successfully", data=user)


def update_user(dto: UserDto):
    try:
        user = db.query(User).filter_by(email=dto.email).first()
        user.name = dto.name
        user.gender = dto.gender
        user.age = dto.age
        user.is_salon_owner = True if dto.is_salon_owner else False
        user.set_password(dto.password)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User Updated successfully"}


def delete_user(dto: UserDto):
    try:
        user = db.query(User).filter_by(email=dto.email).first()
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "User deleted successfully"}


def login_user(login: Login):
    try:
        user = db.query(User).filter_by(email=login.email).first()
        jwt_token = ""
        if user.check_password(login.password):
            jwt_token = jwt.generate_jwt(user)
        else:
            return {"status": 500, "message": "Invalid Username Or Password"}
    except Exception as e:
        return {"status": 500, "message": e}
    else:
        return {"status": 200, "message": "Successfully logged in", "data": {"token": jwt_token}}
