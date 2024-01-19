from pydantic import BaseModel

class Service(BaseModel):
    id: int
    name: str
    price: float
    duration: int  # Duration in minutes
    salon_id: int  # Foreign key to Salon

    class Config:
        orm_mode = True
