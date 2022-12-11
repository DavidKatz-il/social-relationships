import fastapi
from sqlalchemy import orm

from app import database, models


async def get_user_by_email(email: str, db_session: orm.Session):
    return db_session.query(models.User).filter(models.User.email == email).first()


async def get_object_by_id(
    obj_id: int, user_id: int, model: database.Base, db_session: orm.Session
):
    obj_db = (
        db_session.query(model)
        .filter_by(owner_id=user_id)
        .filter(model.id == obj_id)
        .first()
    )

    if obj_db is None:
        raise fastapi.HTTPException(status_code=404, detail="Object does not exist.")

    return obj_db


async def get_object_by_name(
    obj_name: str, user_id: int, model: database.Base, db_session: orm.Session
):
    return (
        db_session.query(model)
        .filter_by(owner_id=user_id)
        .filter(model.name == obj_name)
        .first()
    )
