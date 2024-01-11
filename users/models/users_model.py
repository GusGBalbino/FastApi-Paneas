from sqlalchemy import Column, Integer, String, Enum
from shared.database import Base
from pydantic import BaseModel, EmailStr
import enum

class UserPermission(enum.Enum):
    Admin = "Admin"
    Default = "Default"

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    lastname = Column(String(20))
    email = Column(String, unique=True)
    password = Column(String(255))
    permission = Column(Enum(UserPermission), default=UserPermission.Default.value)