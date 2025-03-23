# src/app/schemas/user.py
from pydantic import BaseModel

class UserSchema(BaseModel):
    user_id: str
    email: str
    name: str

    class Config:
        orm_mode = True
