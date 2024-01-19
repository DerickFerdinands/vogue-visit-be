from pydantic import BaseModel
class UserDto(BaseModel):
    name: str
    gender:str
    age:int
    email: str
    password: str
    is_salon_owner: bool

