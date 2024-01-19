from pydantic import BaseModel

class Appointment(BaseModel):
    id: int
    user_id: int  # Foreign key to User (customer)
    service_id: int  # Foreign key to Service
    salon_id: int  # Foreign key to Salon
    start_time: str  # Format: "YYYY-MM-DD HH:MM"

    class Config:
        orm_mode = True
