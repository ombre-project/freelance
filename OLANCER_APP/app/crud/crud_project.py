from typing import Any, Dict, Union, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectProf, ProjectTaken, ProjectFinal
from sqlalchemy import and_ , or_, false

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):

    def take_project(self, db: Session, id: int, db_obj: Project, obj_in: Union[ProjectTaken, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


    def finish_project(self, db: Session, id: int, db_obj: Project, obj_in: ProjectFinal):
        update_data = obj_in.dict(exclude_unset=True)
        print("update_data : ", update_data)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_all_projects_not_finish(self, db: Session, user_id: int) -> List[Project]:
        return db.query(Project).filter(and_(Project.is_taken == False, Project.project_offer_id != user_id)).all()

    def search_project(self, db: Session, query: str,  user_id: int):
        return db.query(Project).filter(or_(Project.name.contains(query), Project.description.contains(query))).filter(and_(Project.is_taken.is_(False), Project.project_offer_id != user_id)).all()

    def get_projects_def_finish(self, db: Session, id: int):
        return db.query(Project).filter(and_(Project.project_offer_id == id, Project.is_pay == True)).all()

    def get_projects_def_not_finish(self, db: Session, id: int):
        return db.query(Project).filter(and_(Project.project_offer_id == id, Project.is_pay == False)).all()

    def get_projects_dev_finish(self, db: Session, id: int):
        return db.query(Project).filter(and_(Project.project_owner_id == id, Project.is_pay == True)).all()

    def get_projects_not_dev_finish(self, db: Session, id: int):
        return db.query(Project).filter(and_(Project.project_owner_id == id, Project.is_pay == False)).all()

    def get_complete_project(self, db: Session, *, id: int):
        return super().get(db, id)

    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
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

    def deliver_project(self, project:Project) -> bool:
        if project.address_of_project_uploaded is not None:
            return True
        else:
            return False

    def final_project(self, project:Project) -> bool:
        return project.is_finish

    def is_taken(self, project:Project) -> bool:
        return project.is_taken


    def update(
        self, db: Session, *, db_obj: Project, obj_in: Union[ProjectUpdate, Dict[str, Any]]
    ) -> Project:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)



project = CRUDProject(Project)
