from typing import Any, Dict, Union, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectProf, ProjectTaken, ProjectFinal
from sqlalchemy import and_ , or_, false

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """
    this class is child of CRUDBase class and contain some method to help us create read update delete the project table from db
    """

    def take_project(self, db: Session, id: int, db_obj: Project, obj_in: Union[ProjectTaken, Dict[str, Any]]):
        """
        this method is designed when a user want to take a project and it update the the record of the project
        :param db: database object of session local
        :type db: Session
        :param id: the current id of record want to update the table
        :type id: int
        :param db_obj: the current record of a table
        :type db_obj: Project
        :param obj_in: the new record of the table
        :type obj_in: Union[ProjectTaken, Dict[str, Any]]
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


    def finish_project(self, db: Session, id: int, db_obj: Project, obj_in: ProjectFinal):
        """
        this method is designed when a user want to finish a project and it update the the record of the project
        :param db: database object of session local
        :type db: Session
        :param id: the current id of record want to update the table
        :type id: int
        :param db_obj: the current record of a table
        :type db_obj: Project
        :param obj_in: the new record of the table
        :type obj_in: ProjectFinal
        :return:
        """
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_all_projects_not_finish(self, db: Session, user_id: int) -> List[Project]:
        """
        this method get all project of a user not finish yet
        :param db: database object of session local
        :type db: Session
        :param id: the current id of user want to get all records they are not finish
        :type id: int
        :return: list of projects object
        :rtype project list
        """
        return db.query(Project).filter(and_(Project.is_taken == False, Project.project_offer_id != user_id)).all()

    def search_project(self, db: Session, query: str,  user_id: int):
        """
        this method get all project the user search and and the word it searched is in the name or description of project
        :param db: database object of session local
        :param query:the word that user search
        :type query: str
        :type db: Session
        :param id: the current id of user
        :type id: int
        :return: list of projects object
        :rtype project list
        """
        return db.query(Project).filter(or_(Project.name.contains(query), Project.description.contains(query))).filter(and_(Project.is_taken.is_(False), Project.project_offer_id != user_id)).all()

    def get_projects_def_finish(self, db: Session, id: int):
        """
        this method get all projects of a user are finish

        :param db: database object of session local
        :type db: Session
        :param id: the current id of user
        :type id: int
        :return: list of projects object
        :rtype project list
        """
        return db.query(Project).filter(and_(Project.project_offer_id == id, Project.is_pay == True)).all()

    def get_projects_def_not_finish(self, db: Session, id: int):
        """
        this method get all project of a user who define it and not finish yet
        :param db: database object of session local
        :type db: Session
        :param id: the current id of user want to get all records they are not finish
        :type id: int
        :return: list of projects object
        :rtype project list
        """
        return db.query(Project).filter(and_(Project.project_offer_id == id, Project.is_pay == False)).all()

    def get_projects_dev_finish(self, db: Session, id: int):
        """
        this method get all project of a user developing and it finish
        :param db: database object of session local
        :type db: Session
        :param id: the current id of user
        :type id: int
        :return: list of projects object
        :rtype project list
        """
        return db.query(Project).filter(and_(Project.project_owner_id == id, Project.is_pay == True)).all()

    def get_projects_not_dev_finish(self, db: Session, id: int):
        """
        this method get all project of a user developing and not finish yet
        :param db: database object of session local
        :type db: Session
        :param id: the current id of user
        :type id: int
        :return: list of projects object
        :rtype project list
        """
        return db.query(Project).filter(and_(Project.project_owner_id == id, Project.is_pay == False)).all()

    def get_complete_project(self, db: Session, *, id: int):
        """
        this method get the current project by id
        :param db: database object of session local
        :type db: Session
        :param id: the current id of project
        :type id: int
        :return: object project
        :rtype: object
        """
        return super().get(db, id)

    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        """
        this method is for insert project to db
        :param db: database object of session local
        :type db: Session
        :param obj_in: the project to add in db
        :type obj_in: ProjectCreate
        :return:
        """
        db_obj = Project(
            name=obj_in.name,
            project_offer_id=obj_in.project_offer_id,
            cost=obj_in.cost,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            description=obj_in.description,
            img_addr=obj_in.img_addr,
            file_addr=obj_in.file_addr,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def final_project(self, project:Project) -> bool:
        """
        this method tell if project is finish or not
        :param project: object of current project
        :type project: Project
        :return: is project finish or not
        :rtype: bool
        """
        return project.is_finish

    def is_taken(self, project:Project) -> bool:
        """
        this method tell if project is taken or not
        :param project: object of current project
        :type project: Project
        :return: is project finish or not
        :rtype: bool
        """
        return project.is_taken


    def update(
        self, db: Session, *, db_obj: Project, obj_in: Union[ProjectUpdate, Dict[str, Any]]
    ) -> Project:
        """
        this method is use to update current project object
        :param db: database object of session local
        :type db: Session
        :param db_obj: the current record of a table
        :type db_obj: ModelType
        :param obj_in: the new record of the table
        :type obj_in: Union[ProjectUpdate, Dict[str, Any]]
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)



project = CRUDProject(Project)
