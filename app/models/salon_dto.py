from typing import Optional

from pydantic import BaseModel, Field

from app.models.user_dto import UserDto


class SalonDto(BaseModel):
    id: Optional[int] = Field(default=0)
    name: str
    description: str
    location: str
    owner_id: int
    salon_owner: Optional[UserDto]
    instagram_url: str
    facebook_url: str
    phone_num: str
    email: str
    img_1: str
    img_2: str
    img_3: str
    img_4: str
    img_5: str
