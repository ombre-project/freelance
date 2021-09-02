from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    this class is the parent class of create read update and delete from db in this app
    :param model: model we want to execute
    :type model: Type[ModelType]
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        this method get the current object in db by id
        :param db: database object of session local
        :type db: Session
        :param id: id of object
        :type id: int
        :return: object
        :rtype: object
        """
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except:
            return db.query(self.model).filter(self.model.id_proj == id).first()


    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        this method get a list of object in db in size between skip to limit
        :param db: database object of session local
        :type db: Session
        :param id: id of object
        :type id: int
        :param skip: objects from skip number
        :type skip: int
        :param limit: objects to limit number
        :type limit: int
        :return: object
        :rtype: object
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        this method to insert a new record
        :param db: database object of session local
        :type db: Session
        :param obj_in: fields of the table
        :type obj_in: CreateSchemaType
        :return:
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        this method update a record in  a table
        :param db: database object of session local
        :type db: Session
        :param db_obj: the current record of a table
        :type db_obj: ModelType
        :param obj_in: the new record of the table
        :type obj_in: Union[UpdateSchemaType, Dict[str, Any]]
        :return:
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        this method delete the current object record in a table
        :param db: database object of session local
        :type db: Session
        :param id: the current id of record want to delete from table
        :type id: int
        :return:
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj