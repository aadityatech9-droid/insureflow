from pydantic import BaseModel ,EmailStr
from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email:EmailStr
    password:str
    role:UserRole=UserRole.customer

class LoginRequest(BaseModel):
    email:EmailStr
    password:str


class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str="bearer"

class UserResponse(BaseModel):
    id:int
    email:str
    role:UserRole

    model_config={"from_attributes":True}
    