from datetime import datetime

import fastapi
import jwt
from passlib.hash import bcrypt
from sqlalchemy import orm

from app import database, models, schemas


JWT_SECRET = "special-jwt-secret"
oauth2schema = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/token")


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate, db: orm.Session):
    user_obj = models.User(
        email=user.email, hashed_password=bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")

    return schemas.User.from_orm(user)


async def get_persons(user: schemas.User, db: orm.Session):
    persons = db.query(models.Person).filter_by(owner_id=user.id)

    return list(map(schemas.Person.from_orm, persons))


async def get_person_by_name(person_name: str, user_id: int, db: orm.Session):
    return (
        db.query(models.Person)
        .filter_by(owner_id=user_id)
        .filter(models.Person.name == person_name)
        .first()
    )


async def validate_person(person: schemas.PersonCreate):
    if not person.name or not person.images or (person.images == "[]"):
        raise fastapi.HTTPException(
            status_code=400, detail="Person must have a name and at least one image."
        )


async def validate_person_name_not_exist(
    person_name: str, user_id: int, db: orm.Session
):
    person_db = await get_person_by_name(
        person_name=person_name, user_id=user_id, db=db
    )
    if person_db:
        raise fastapi.HTTPException(status_code=400, detail="Person already exist.")


async def create_person(
    user: schemas.User, db: orm.Session, person: schemas.PersonCreate
):
    await validate_person(person=person)
    await validate_person_name_not_exist(
        person_name=person.name, user_id=user.id, db=db
    )

    person = models.Person(**person.dict(), owner_id=user.id)
    db.add(person)
    db.commit()
    db.refresh(person)
    return schemas.Person.from_orm(person)


async def _person_selector(person_id: int, user_id: int, db: orm.Session):
    person = (
        db.query(models.Person)
        .filter_by(owner_id=user_id)
        .filter(models.Person.id == person_id)
        .first()
    )

    if person is None:
        raise fastapi.HTTPException(status_code=404, detail="Person does not exist")

    return person


async def get_person(person_id: int, user: schemas.User, db: orm.Session):
    person = await _person_selector(person_id=person_id, user_id=user.id, db=db)

    return schemas.Person.from_orm(person)


async def delete_person(person_id: int, user: schemas.User, db: orm.Session):
    person_db = await _person_selector(person_id=person_id, user_id=user.id, db=db)

    db.delete(person_db)
    db.commit()


async def update_person(
    person_id: int, person: schemas.PersonCreate, user: schemas.User, db: orm.Session
):
    person_db = await _person_selector(person_id=person_id, user_id=user.id, db=db)
    if person.name != person_db.name:
        await validate_person_name_not_exist(
            person_name=person.name, user_id=user.id, db=db
        )

    person_db.name = person.name
    person_db.images = person.images
    person_db.datetime_updated = datetime.utcnow()

    await validate_person(person=person_db)
    db.commit()
    db.refresh(person_db)

    return schemas.Person.from_orm(person_db)
