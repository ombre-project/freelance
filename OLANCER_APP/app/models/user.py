from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Date

from app.db.base_class import Base

if TYPE_CHECKING:
    from .project import Project


class User(Base):
    """
    this is the model of project use in this app
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    password_omb = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    wallet_address = Column(String, nullable=False, unique=True)
    born = Column(Date, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    address = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    resume_address = Column(String, nullable=True)
    img_address = Column(String, nullable=True)
    username_omb = Column(String, nullable=False, unique=True)