from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String, Float, Date, ForeignKey
from app.db.base_class import Base
if TYPE_CHECKING:
    from .user import User


class Project(Base):
    __tablename__ = "projects"
    id_proj = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    img_addr = Column(String, nullable=True)
    file_addr = Column(String, nullable=True)
    description = Column(String, nullable=False)
    is_finish = Column(Boolean(), default=False)
    project_owner_id = Column(Integer,  ForeignKey("users.id"))
    project_offer_id = Column(Integer,  ForeignKey("users.id"))
    cost = Column(Float, nullable=False, default=0.0)
    start_date = Column(Date, nullable=False)
    is_pay = Column(Boolean, default=False)
    is_taken = Column(Boolean, default=False)
    common = Column(Integer, nullable=True)
    common_describe = Column(String, nullable=True)
    end_date = Column(Date, nullable=True)
    address_of_project_uploaded = Column(String, nullable=True)