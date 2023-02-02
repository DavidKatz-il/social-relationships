import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Union

import fastapi
from sqlalchemy import orm

from app import models, schemas
from app.reports import InterfaceReport, report_factory
from app.services.utils.db import get_object_by_id, get_object_by_name
from app.services.utils.face_recognition import (
    create_match_faces,
    get_images,
    get_match_faces_by_image,
    get_match_faces_by_student,
    get_students_list,
)


class Data:
    student_images: Dict[str, List[str]]
    image_students: Dict[str, List[str]]
    all_student_names: List[str]
    images: List[Dict[str, Union[List[str], List[List[int]]]]]

    def __init__(self, user: schemas.User, db_session: orm.Session):
        self.user = user
        self.db_session = db_session

    async def set_all(self):
        await asyncio.gather(
            self._set_student_images(),
            self._set_image_students(),
            self._set_all_student_names(),
            self._set_images(),
        )

    async def _set_student_images(self):
        self.student_images = await get_match_faces_by_student(
            self.user, self.db_session
        )

    async def _set_image_students(self):
        self.image_students = await get_match_faces_by_image(self.user, self.db_session)

    async def _set_all_student_names(self):
        self.all_student_names = await get_students_list(self.user, self.db_session)

    async def _set_images(self):
        self.images = await get_images(self.user, self.db_session)

    @staticmethod
    async def to_report_info(
        report: List[Dict[str, Union[str, int]]]
    ) -> Dict[Union[int, str], List]:
        if report:
            if ["Image"] == list(report[0].keys()):
                return {"images": list(row["Image"] for row in report)}
            columns = {0: list(report[0].keys())}
            rows = {idx: list(row.values()) for idx, row in enumerate(report, start=1)}
            return {**columns, **rows}
        return {}


async def save_report_in_db(
    name_of_report,
    report_info,
    user: schemas.User,
    db_session: orm.Session,
):
    report = schemas.ReportCreate(
        name=name_of_report,
        info=report_info,
    )
    report = models.Report(**report.dict(), owner_id=user.id)
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)


async def create_update_reports(user: schemas.User, db_session: orm.Session):
    if (db_session.query(models.Image).filter_by(owner_id=user.id).count() == 0) or (
        db_session.query(models.Student).filter_by(owner_id=user.id).count() == 0
    ):
        raise fastapi.HTTPException(
            status_code=400, detail="There must be at least one student and one image."
        )

    await create_match_faces(user, db_session)
    data = Data(user=user, db_session=db_session)
    await data.set_all()

    for creator in report_factory.creators():
        report_creator = creator()
        report_db = await get_object_by_name(
            obj_name=report_creator.name,
            user_id=user.id,
            model=models.Report,
            db_session=db_session,
        )
        if report_db:
            await update_report(report_db.id, user, db_session, data)
        else:
            await create_report(report_creator, user, db_session, data)

    return {"message", "Successfully finished reports creating and update."}


async def create_report(
    report_creator: InterfaceReport,
    user: schemas.User,
    db_session: orm.Session,
    data: Optional[Data] = None,
):
    data = data or Data(user, db_session)
    report = report_creator.create(data)
    report_info = await data.to_report_info(report)
    await save_report_in_db(report_creator.name, report_info, user, db_session)


async def get_reports(user: schemas.User, db_session: orm.Session):
    report = db_session.query(models.Report).filter_by(owner_id=user.id)
    return list(map(schemas.Report.from_orm, report))


async def get_specific_report(
    user: schemas.User, db_session: orm.Session, report_id: schemas.Report
):
    report_db = await get_object_by_id(
        obj_id=report_id, user_id=user.id, model=models.Report, db_session=db_session
    )

    return schemas.Report.from_orm(report_db)


async def delete_report(report_id: int, user: schemas.User, db_session: orm.Session):
    report_db = await get_object_by_id(
        obj_id=report_id, user_id=user.id, model=models.Report, db_session=db_session
    )

    db_session.delete(report_db)
    db_session.commit()


async def update_report(
    report_id: int,
    user: schemas.User,
    db_session: orm.Session,
    data: Optional[Data] = None,
):
    data = data or Data(user, db_session)
    report_db = await get_object_by_id(
        obj_id=report_id, user_id=user.id, model=models.Report, db_session=db_session
    )

    report_creator = report_factory.get_report_creator(report_db.name)
    report_db.info = await data.to_report_info(report_creator.create(data))
    report_db.datetime_updated = datetime.utcnow()

    db_session.commit()
    db_session.refresh(report_db)

    return schemas.Report.from_orm(report_db)


async def get_reports_info(user: schemas.User, db_session: orm.Session):
    reports = (
        db_session.query(models.Report)
        .filter_by(owner_id=user.id)
        .with_entities(models.Report.id, models.Report.name)
    )
    return list(map(schemas.ReportInfo.from_orm, reports))
