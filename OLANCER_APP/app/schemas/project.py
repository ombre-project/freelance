from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from app.core.config import as_form

@as_form
class ProjectProf(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file_addr: Optional[str] = None
    img_addr: Optional[str] = None
    cost: Optional[str] = None
    end_date: Optional[str] = None
    project_offer_id: Optional[int] = None
    start_date: Optional[str] = None

# Shared properties
class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_offer_id: Optional[int] = None
    file_addr: Optional[str] = None
    img_addr: Optional[str] = None
    cost: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ProjectTaken(ProjectBase):
    project_owner_id: Optional[int] = None
    is_pay: Optional[bool] = False
    is_taken: Optional[bool] = False
    address_of_project_uploaded: Optional[str] = None

class ProjectFinal(ProjectTaken):
    common: Optional[int] = 0
    common_describe: Optional[str] = None
    is_finish: Optional[bool] = False


# Properties to receive via API on creation
class ProjectCreate(ProjectBase):
    pass


# Properties to receive via API on update
class ProjectUpdate(ProjectBase):
    pass
#     password: Optional[str] = None


class ProjectInDBBase(ProjectBase):
    id_proj: Optional[int] = None
    project_owner_id: Optional[int] = None
    project_offer_id: Optional[int] = None
    class Config:
        orm_mode = True


# Additional properties to return via API
class Project(ProjectInDBBase):
    pass


# Additional properties stored in DB
class ProjectInDB(ProjectInDBBase):
    pass
    # hashed_password: str

