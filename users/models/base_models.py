
from pydantic import BaseModel, EmailStr, SecretStr, Field

from typing import Optional

from users.models.users_model import UserPermission

class UserResponse(BaseModel):
    id: int
    name: str
    lastname: str
    email: EmailStr
    permission: str 
    
    class Config:
        from_attributes = True
    
class UserCreateRequest(BaseModel):
    name: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    email: str = Field(..., example="john.doe@example.com")
    password: SecretStr = Field(..., example="strongpassword")

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "lastname": "Doe",
                "email": "john.doe@example.com",
                "password": "strongpassword"
            }
        }
    
class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    permission: Optional[UserPermission] = None

class Login(BaseModel):
    email: str
    password: str