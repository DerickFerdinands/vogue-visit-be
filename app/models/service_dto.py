from typing import Optional

from pydantic import BaseModel, Field

from app.models.salon_dto import SalonDto


class ServiceDto(BaseModel):
    id:  Optional[int] = Field(default=None)
    name: str
    description: str
    price: int
    img_1: str
    img_2: str
    img_3: str
    img_4: str
    img_5: str
    slot_count: int
    salon_id: Optional[int] = Field(default=None)
    salon: Optional[SalonDto] = Field(default=None)

    class Config:
        orm_mode = True
