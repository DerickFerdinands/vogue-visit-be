from typing import Optional

from pydantic import BaseModel, Field


class UserDto(BaseModel):
    id: Optional[int]
    name: str
    gender:str
    age:int
    email: str
    password: str
    is_salon_owner: Optional[bool] = Field(default=False)

