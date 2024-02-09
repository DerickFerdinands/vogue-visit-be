from datetime import datetime, timedelta

from fastapi import HTTPException
from datetime import date
from app.database.db import get_db, Salon, Service, TimeSlot
from app.mappers.service_mapper import map_dto_to_service
from app.models.salon_dto import SalonDto
from app.models.service_dto import ServiceDto
from app.models.time_slot_dto import TimeSlotDto
from app.models.time_slot_rq import TimeSlotRq
from app.models.user_dto import UserDto

# db_session = get_db()
db = get_db()


def get_all_slots():
    try:
        print("Getting all slots...")
        result = db.query(TimeSlot).all()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        # result.foreach()
        return {"status": 200, "message": "Successfully fetched all Time Slots", "data": result}


def get_slots_for_date(date: str, user: UserDto):

    try:
        validated_date = datetime.strptime(date, '%Y-%m-%d').date()
        salon = db.query(Salon).filter_by(owner_id=user.id).first()
        slots = db.query(TimeSlot).filter_by(salon_id=salon.id, date=validated_date).all()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        # result.foreach()
        return {"status": 200, "message": "Successfully fetched all Time Slots for the dat", "data": slots}


def get_slots_for_date_by_salon_id(salon_id: int, date: str):

    try:
        validated_date = datetime.strptime(date, '%Y-%m-%d').date()
        slots = db.query(TimeSlot).filter_by(salon_id=salon_id, date=validated_date).all()
    except Exception as e:
        print(e)
        return {"status": 500, "message": e}
    else:
        # result.foreach()
        return {"status": 200, "message": "Successfully fetched all Time Slots for the dat", "data": slots}

def get_dates_and_slots(user: UserDto):
    try:
        # Get today's date
        today_date = date.today()

        # Format today's date as a string
        validated_date = today_date.strftime('%Y-%m-%d')

        # Query the salon
        salon = db.query(Salon).filter_by(owner_id=user.id).first()

        # Filter and get unique dates
        slots = db.query(TimeSlot.date).filter(
            (TimeSlot.salon_id == salon.id) & (TimeSlot.date >= validated_date)
        ).distinct().all()

        # Extract unique dates from the result
        unique_dates = [result[0] for result in slots]
    except Exception as e:
        print(e)
        return {"status": 500, "message": str(e)}
    else:
        return {"status": 200, "message": "Successfully fetched unique dates for Time Slots", "data": unique_dates}


def get_dates_by_salon_id(salonId: int):
    try:
        # Get today's date
        today_date = date.today()

        # Format today's date as a string
        validated_date = today_date.strftime('%Y-%m-%d')

        # Filter and get unique dates
        slots = db.query(TimeSlot.date).filter(
            (TimeSlot.salon_id == salonId) & (TimeSlot.date >= validated_date)
        ).distinct().all()

        # Extract unique dates from the result
        unique_dates = [result[0] for result in slots]
    except Exception as e:
        print(e)
        return {"status": 500, "message": str(e)}
    else:
        return {"status": 200, "message": "Successfully fetched unique dates for Time Slots", "data": unique_dates}

def save_slots(slot_rq: TimeSlotRq, user: UserDto):
    print(slot_rq)
    try:
        # Validate date and time format
        try:
            date = datetime.strptime(slot_rq.date, '%Y-%m-%d').date()
            start_time = datetime.strptime(slot_rq.start_time, '%H:%M').time()
            end_time = datetime.strptime(slot_rq.end_time, '%H:%M').time()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date or time format")

        # Fetch the salon associated with the user
        salon = db.query(Salon).filter_by(owner_id=user.id).first()

        if not salon:
            raise HTTPException(status_code=404, detail="Salon not found")

        # Calculate time slots
        current_time = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        time_slots = []
        while current_time < end_datetime:
            time_slots.append(TimeSlotDto(
                salon_id=salon.id,
                date=date,
                start_time=current_time.time(),
                end_time=(current_time + timedelta(minutes=15)).time(),
                is_booked=False
            ))
            current_time += timedelta(minutes=15)

        # Save time slots to the database
        db.bulk_save_objects([TimeSlot(**slot.dict()) for slot in time_slots])
        db.commit()

        return {"status": 200, "message": "Time slots created successfully"}

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# def get_slot(id: int):
#     try:
#         service = db.query(Service).filter_by(id=id).first()
#     except Exception as e:
#         print(e)
#         return {"status": 500, "message": e}
#     else:
#         return {"status": 200, "message": "salon Fetched successfully", "data": service}
#
#
# def update_slot(dto: ServiceDto, user: UserDto):
#     try:
#
#         # Find the service in the salon's services
#         service = db.query(Service).filter_by(id=dto.id).first()
#
#         if service:
#             # Update service attributes using ServiceDto
#             service.name = dto.name
#             service.description = dto.description
#             service.price = dto.price
#             service.img_1 = dto.img_1
#             service.img_2 = dto.img_2
#             service.img_3 = dto.img_3
#             service.img_4 = dto.img_4
#             service.img_5 = dto.img_5
#             service.slot_count = dto.slot_count
#             db.commit()
#             return {"status": 200, "message": "Salon updated successfully"}
#         else:
#             return {"status": 404, "message": "Salon not found"}
#     except Exception as e:
#         print(e)
#         db.rollback()
#         return {"status": 500, "message": str(e)}
#
#
# def delete_slot(dto: ServiceDto,user: UserDto):
#     try:
#         salon = db.query(Service).filter_by(id=dto.id).first()
#         db.delete(salon)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         return {"status": 500, "message": e}
#     else:
#         return {"status": 200, "message": "User deleted successfully"}
