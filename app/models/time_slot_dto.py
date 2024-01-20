from pydantic import BaseModel
from datetime import time, date

class TimeSlotDto(BaseModel):
    salon_id: int
    date: date
    start_time: time
    end_time: time
    is_booked: bool

    class Config:
        orm_mode = True
