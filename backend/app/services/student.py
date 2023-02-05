import json
from datetime import datetime
from typing import List, Tuple, Union

import fastapi
from sqlalchemy import orm

from app import models, schemas
from app.core_utils.const import ExceptionMessagesConst
from app.core_utils.exceptions import ImageFaceError
from app.core_utils.face_recognition import (
    get_locations_and_encodings_from_images_with_only_one_face,
)
from app.services.utils.db import get_object_by_id, get_object_by_name
from app.services.utils.validations import (
    validate_student,
    validate_student_name_not_exist,
)


async def get_students(user: schemas.User, db_session: orm.Session):
    students = db_session.query(models.Student).filter_by(owner_id=user.id)

    return list(map(schemas.Student.from_orm, students))


async def get_student(student_id: int, user: schemas.User, db_session: orm.Session):
    student_db = await get_object_by_id(
        obj_id=student_id, user_id=user.id, model=models.Student, db_session=db_session
    )

    return schemas.Student.from_orm(student_db)


async def get_locations_and_encodings_from_images(
    images: List[str],
) -> Tuple[Union[list, List[List[int]]], Union[list, List[List[float]]]]:
    try:
        return await get_locations_and_encodings_from_images_with_only_one_face(images)
    except ImageFaceError as exc:
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.STUDENT_IMAGE_ONE_FACE.value
        ) from exc


async def create_student(
    user: schemas.User, db_session: orm.Session, student: schemas.StudentCreate
):
    await validate_student_name_not_exist(
        student_name=student.name, user_id=user.id, db_session=db_session
    )

    locations, encodings = await get_locations_and_encodings_from_images(
        images=json.loads(student.images)
    )
    face_student = schemas.FaceStudentCreate(
        face_locations=locations, face_encodings=encodings, name=student.name
    )

    student = models.Student(**student.dict(), owner_id=user.id)
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    face_student = await create_face_student(
        user=user, db_session=db_session, face_student=face_student
    )

    return schemas.Student.from_orm(student)


async def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    user: schemas.User,
    db_session: orm.Session,
):
    student_db = await get_object_by_id(
        obj_id=student_id, user_id=user.id, model=models.Student, db_session=db_session
    )
    face_student_db = await get_object_by_name(
        obj_name=student_db.name,
        user_id=user.id,
        model=models.FaceStudent,
        db_session=db_session,
    )

    if student.name != student_db.name:
        await validate_student_name_not_exist(
            student_name=student.name, user_id=user.id, db_session=db_session
        )
        student_db.name = student.name

    if student.images != student_db.images:
        student_db.images = student.images
        locations, encodings = await get_locations_and_encodings_from_images(
            images=json.loads(student.images)
        )
    else:
        locations, encodings = (
            face_student_db.face_locations,
            face_student_db.face_encodings,
        )

    student_db.datetime_updated = datetime.utcnow()
    await validate_student(student=student_db)

    face_student = schemas.FaceStudentCreate(
        face_locations=locations, face_encodings=encodings, name=student_db.name
    )
    face_student = await update_face_student(
        face_student_id=face_student_db.id,
        face_student=face_student,
        user=user,
        db_session=db_session,
    )

    db_session.commit()
    db_session.refresh(student_db)

    return schemas.Student.from_orm(student_db)


async def delete_student(student_id: int, user: schemas.User, db_session: orm.Session):
    student_db = await get_object_by_id(
        obj_id=student_id, user_id=user.id, model=models.Student, db_session=db_session
    )

    db_session.delete(student_db)
    db_session.commit()

    face_student_db = await get_object_by_name(
        obj_name=student_db.name,
        user_id=user.id,
        model=models.FaceStudent,
        db_session=db_session,
    )
    await delete_face_student(
        face_student_id=face_student_db.id, user=user, db_session=db_session
    )


async def create_face_student(
    user: schemas.User, db_session: orm.Session, face_student: schemas.FaceStudentCreate
):
    face_student = models.FaceStudent(**face_student.dict(), owner_id=user.id)

    db_session.add(face_student)
    db_session.commit()
    db_session.refresh(face_student)
    return schemas.FaceStudent.from_orm(face_student)


async def update_face_student(
    face_student_id: int,
    face_student: schemas.FaceStudentCreate,
    user: schemas.User,
    db_session: orm.Session,
):
    face_student_db = await get_object_by_id(
        obj_id=face_student_id,
        user_id=user.id,
        model=models.FaceStudent,
        db_session=db_session,
    )

    face_student_db.name = face_student.name
    face_student_db.face_locations = face_student.face_locations
    face_student_db.face_encodings = face_student.face_encodings
    face_student_db.datetime_updated = datetime.utcnow()

    db_session.commit()
    db_session.refresh(face_student_db)

    return schemas.FaceStudent.from_orm(face_student_db)


async def delete_face_student(
    face_student_id: int, user: schemas.User, db_session: orm.Session
):
    face_student_db = await get_object_by_id(
        obj_id=face_student_id,
        user_id=user.id,
        model=models.FaceStudent,
        db_session=db_session,
    )

    db_session.delete(face_student_db)
    db_session.commit()


async def get_faces_students(user: schemas.User, db_session: orm.Session):
    faces_students = db_session.query(models.FaceStudent).filter_by(owner_id=user.id)

    return list(map(schemas.FaceStudent.from_orm, faces_students))


async def get_face_student(
    face_student_id: int, user: schemas.User, db_session: orm.Session
):
    face_student_db = await get_object_by_id(
        obj_id=face_student_id,
        user_id=user.id,
        model=models.FaceStudent,
        db_session=db_session,
    )

    return schemas.FaceStudent.from_orm(face_student_db)
