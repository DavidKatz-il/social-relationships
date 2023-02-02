import re

import fastapi
from sqlalchemy import orm

from app import models, schemas
from app.core_utils.const import ExceptionMessagesConst
from app.services.utils.db import get_object_by_name, get_user_by_email


async def validate_email(email: str, db_session: orm.Session):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not email or not re.match(email_regex, email):
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.EMAIL_INVALID.value
        )

    if await get_user_by_email(email=email, db_session=db_session):
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.EMAIL_EXIST.value
        )


async def validate_hashed_password(hashed_password: str):
    min_pass_len = 6
    if len(hashed_password) < min_pass_len:
        raise fastapi.HTTPException(
            status_code=400,
            detail=ExceptionMessagesConst.PASSWORD_REQUIREMENTS.value.format(
                min_pass_len
            ),
        )


async def validate_user(user: schemas.UserCreate, db_session: orm.Session):
    await validate_email(user.email, db_session)
    await validate_hashed_password(user.hashed_password)


async def validate_student(student: schemas.StudentCreate):
    if not student.name or not student.images or (student.images == "[]"):
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.STUDENT_REQUIREMENTS.value
        )


async def validate_student_name_not_exist(
    student_name: str, user_id: int, db_session: orm.Session
):
    student_db = await get_object_by_name(
        obj_name=student_name,
        user_id=user_id,
        model=models.Student,
        db_session=db_session,
    )
    if student_db:
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.STUDENT_EXIST.value
        )


async def validate_image(image: schemas.ImageCreate):
    if not image.name or not image.image:
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.IMAGE_REQUIREMENTS.value
        )


async def validate_image_name_not_exist(
    image_name: str, user_id: int, db_session: orm.Session
):
    image_db = await get_object_by_name(
        obj_name=image_name, user_id=user_id, model=models.Image, db_session=db_session
    )
    if image_db:
        raise fastapi.HTTPException(
            status_code=400, detail=ExceptionMessagesConst.IMAGE_EXIST.value
        )
