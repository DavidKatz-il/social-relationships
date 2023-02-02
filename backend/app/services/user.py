from datetime import datetime

import fastapi
import jwt
from passlib.hash import bcrypt
from sqlalchemy import orm

from app import models, schemas
from app.core_utils.const import UserConst
from app.services.database import get_db_session
from app.services.utils.db import get_user_by_email
from app.services.utils.validations import (
    validate_email,
    validate_hashed_password,
    validate_user,
)

oauth2schema = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/token")


async def create_user(user: schemas.UserCreate, db_session: orm.Session):
    await validate_user(user=user, db_session=db_session)

    user.hashed_password = bcrypt.hash(user.hashed_password)
    user_obj = models.User(**user.dict())

    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)
    return user_obj


async def update_user(
    user_update: schemas.UserUpdate, user: schemas.User, db_session: orm.Session
):
    user_db = db_session.query(models.User).filter(models.User.id == user.id).first()

    if user_update.email and user_update.email != user_db.email:
        await validate_email(user_update.email, db_session=db_session)
        user_db.email = user_update.email
    if (
        user_update.hashed_password
        and user_update.hashed_password != user_db.hashed_password
    ):
        await validate_hashed_password(user_update.hashed_password)
        user_db.hashed_password = bcrypt.hash(user_update.hashed_password)
    if user_update.teacher_name:
        user_db.teacher_name = user_update.teacher_name
    if user_update.school_name:
        user_db.school_name = user_update.school_name

    user_db.datetime_updated = datetime.utcnow()

    db_session.commit()
    db_session.refresh(user_db)

    return schemas.User.from_orm(user_db)


async def authenticate_user(email: str, password: str, db_session: orm.Session):
    user = await get_user_by_email(email=email, db_session=db_session)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.User) -> dict:
    user_obj = schemas.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), UserConst.JWT_SECRET.value)
    token_data = {"access_token": token, "token_type": UserConst.TOKEN_TYPE.value}
    return token_data


async def get_current_user(
    db_session: orm.Session = fastapi.Depends(get_db_session),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, UserConst.JWT_SECRET.value, algorithms=["HS256"])
        user = db_session.query(models.User).get(payload["id"])
    except Exception as exception:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password."
        ) from exception

    return schemas.User.from_orm(user)


async def get_user_info(user: schemas.User, db_session: orm.Session):
    students_count = (
        db_session.query(models.Student).filter_by(owner_id=user.id).count()
    )
    images_count = db_session.query(models.Image).filter_by(owner_id=user.id).count()
    user_info = {"students_count": students_count, "images_count": images_count}
    return schemas.UserInfo(**user_info)
