from pydantic import BaseModel, Field

class Salon(BaseModel):
    id: int
    name: str
    location: str
    owner_id: int  # Foreign key to User (salon owner)

    class Config:
        orm_mode = True
