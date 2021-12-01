from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserProf


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        get current user by email
        :param db: database object of session local
        :type db: Session
        :param email: email of user
        :type email: str
        :return: get current user
        :rtype: object
        """
        return db.query(User).filter(User.email == email).first()

    def update_complete_user(self, db: Session, id: int, db_obj: User, obj_in: UserProf):
        """
        update the current user
        :param db: database object of session local
        :type db: Session
        :param id:
        :param db_obj: the current user
        :type db_obj: User
        :param obj_in: the new record for the current user
        :type obj_in: UserProf
        :return:
        """
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_complete_user(self, db: Session, *, id: int):
        """
        get the current user
        :param db: database object of session local
        :type db: Session
        :param id: id of the current user
        :type id: int
        :return: get object of current user
        :rtype: object
        """
        return super().get(db, id)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        insert new user
        :param db: database object of session local
        :type db: Session
        :param obj_in: the new record for the new user
        :type obj_in: UserCreate
        :return:
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            wallet_address=obj_in.wallet_address,
            username_omb=obj_in.username_omb,
            password_omb=obj_in.password_omb
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        update the user record
        :param db: database object of session local
        :type db: Session
        :param db_obj: the current user
        :type db_obj: User
        :param obj_in: the new record for the current user
        :type obj_in: Union[UserUpdate, Dict[str, Any]]
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        check authenticate of the user
        :param db: database object of session local
        :type db: Session
        :param email: email of user
        :type email: str
        :param password: the password of the user
        :type : str
        :return:
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """
        complete later
        :param user:
        :return:
        """
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """
        complete later
        :param user:
        :return:
        """
        return user.is_superuser


user = CRUDUser(User)
