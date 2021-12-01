from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from app.core.config import as_form

@as_form
class UserProf(BaseModel):
    """
    to get request from client profile page
    """
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None
    born: Optional[date] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    bio: Optional[str] = None
    resume_address: Optional[str] = None
    img_address: Optional[str] = None

# Shared properties
class UserBase(BaseModel):
    """
    Shared properties
    """
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    Properties to receive via API on creation
    """
    email: EmailStr
    password: str
    password_omb: str
    username_omb: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """
    Properties to receive via API on update
    """
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    """
    Additional properties to return via API
    """
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    """
    Additional properties stored in DB
    """
    hashed_password: str

