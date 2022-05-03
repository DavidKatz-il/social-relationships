import json
from datetime import datetime
from urllib.request import urlopen

import numpy as np
import fastapi
import jwt
import face_recognition
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


async def _get_object_by_id(obj_id: int, user_id: int, model: database.Base, db: orm.Session):
    obj_db = (
        db.query(model)
        .filter_by(owner_id=user_id)
        .filter(model.id == obj_id)
        .first()
    )

    if obj_db is None:
        raise fastapi.HTTPException(status_code=404, detail="Object does not exist.")

    return obj_db


async def _get_object_by_name(obj_name: str, user_id: int, model: database.Base, db: orm.Session):
    return (
        db.query(model)
        .filter_by(owner_id=user_id)
        .filter(model.name == obj_name)
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
    person_db = await _get_object_by_name(
        obj_name=person_name, user_id=user_id, model=models.Person, db=db
    )
    if person_db:
        raise fastapi.HTTPException(status_code=400, detail="Person already exist.")


async def get_persons(user: schemas.User, db: orm.Session):
    persons = db.query(models.Person).filter_by(owner_id=user.id)

    return list(map(schemas.Person.from_orm, persons))


async def get_person(person_id: int, user: schemas.User, db: orm.Session):
    person_db = await _get_object_by_id(obj_id=person_id, user_id=user.id, model=models.Person, db=db)

    return schemas.Person.from_orm(person_db)


async def create_person(
    user: schemas.User, db: orm.Session, person: schemas.PersonCreate
):
    await validate_person(person=person)
    await validate_person_name_not_exist(
        person_name=person.name, user_id=user.id, db=db
    )

    locations, encodings = await get_locations_and_encodings_from_images(
        images=json.loads(person.images)
    )
    face_person = schemas.FacePersonCreate(
        face_locations=locations, face_encodings=encodings, name=person.name
    )

    person = models.Person(**person.dict(), owner_id=user.id)
    db.add(person)
    db.commit()
    db.refresh(person)
    face_person = await create_face_person(user=user, db=db, face_person=face_person)

    return schemas.Person.from_orm(person)


async def update_person(
    person_id: int, person: schemas.PersonCreate, user: schemas.User, db: orm.Session
):
    person_db = await _get_object_by_id(obj_id=person_id, user_id=user.id, model=models.Person, db=db)
    if person.name != person_db.name:
        await validate_person_name_not_exist(
            person_name=person.name, user_id=user.id, db=db
        )

    person_db.name = person.name
    person_db.images = person.images
    person_db.datetime_updated = datetime.utcnow()

    await validate_person(person=person_db)
    locations, encodings = await get_locations_and_encodings_from_images(
        images=json.loads(person.images)
    )
    face_person = schemas.FacePersonCreate(
        face_locations=locations, face_encodings=encodings, name=person.name
    )
    face_person_db = await _get_object_by_name(obj_name=person_db.name, user_id=user.id, model=models.FacePerson, db=db)
    face_person = await update_face_person(face_person_id=face_person_db.id, face_person=face_person, user=user, db=db)

    db.commit()
    db.refresh(person_db)

    return schemas.Person.from_orm(person_db)


async def delete_person(person_id: int, user: schemas.User, db: orm.Session):
    person_db = await _get_object_by_id(obj_id=person_id, user_id=user.id, model=models.Person, db=db)

    db.delete(person_db)
    db.commit()

    face_person_db = await _get_object_by_name(obj_name=person_db.name, user_id=user.id, model=models.FacePerson, db=db)
    await delete_face_person(face_person_id=face_person_db.id, user=user, db=db)

async def validate_image(image: schemas.ImageCreate):
    if not image.name or not image.image:
        raise fastapi.HTTPException(
            status_code=400, detail="Image must have a name and a image."
        )


async def validate_image_name_not_exist(
    image_name: str, user_id: int, db: orm.Session
):
    image_db = await _get_object_by_name(
        obj_name=image_name, user_id=user_id, model=models.Image, db=db
    )
    if image_db:
        raise fastapi.HTTPException(status_code=400, detail="Image already exist.")


async def get_images(user: schemas.User, db: orm.Session):
    images = db.query(models.Image).filter_by(owner_id=user.id)

    return list(map(schemas.Image.from_orm, images))


async def get_image(image_id: int, user: schemas.User, db: orm.Session):
    image_db = await _get_object_by_id(obj_id=image_id, user_id=user.id, model=models.Image, db=db)

    return schemas.Image.from_orm(image_db)


async def create_image(
    user: schemas.User, db: orm.Session, image: schemas.ImageCreate
):
    await validate_image(image=image)
    await validate_image_name_not_exist(
        image_name=image.name, user_id=user.id, db=db
    )

    locations, encodings = await get_locations_and_encodings_from_image(
        image_base64=image.image
    )
    face_image = schemas.FaceImageCreate(
        face_locations=locations, face_encodings=encodings, name=image.name, person_names=[]
    )
    
    image = models.Image(**image.dict(), owner_id=user.id)
    db.add(image)
    db.commit()
    db.refresh(image)
    
    face_image = await create_face_image(user=user, db=db, face_image=face_image)
    
    return schemas.Image.from_orm(image)


async def delete_image(image_id: int, user: schemas.User, db: orm.Session):
    image_db = await _get_object_by_id(obj_id=image_id, user_id=user.id, model=models.Image, db=db)

    db.delete(image_db)
    db.commit()

    face_image_db = await _get_object_by_name(obj_name=image_db.name, user_id=user.id, model=models.FaceImage, db=db)
    await delete_face_image(face_image_id=face_image_db.id, user=user, db=db)


async def get_faces_persons(user: schemas.User, db: orm.Session):
    faces_persons = db.query(models.FacePerson).filter_by(owner_id=user.id)

    return list(map(schemas.FacePerson.from_orm, faces_persons))


async def get_face_person(face_person_id: int, user: schemas.User, db: orm.Session):
    face_person_db = await _get_object_by_id(obj_id=face_person_id, user_id=user.id, model=models.FacePerson, db=db)

    return schemas.FacePerson.from_orm(face_person_db)


async def create_face_person(
    user: schemas.User, db: orm.Session, face_person: schemas.FacePersonCreate
):
    face_person = models.FacePerson(**face_person.dict(), owner_id=user.id)

    db.add(face_person)
    db.commit()
    db.refresh(face_person)
    return schemas.FacePerson.from_orm(face_person)


async def update_face_person(
    face_person_id: int, face_person: schemas.FacePersonCreate, user: schemas.User, db: orm.Session
):
    face_person_db = await _get_object_by_id(obj_id=face_person_id, user_id=user.id, model=models.FacePerson, db=db)

    face_person_db.name = face_person.name
    face_person_db.face_locations = face_person.face_locations
    face_person_db.face_encodings = face_person.face_encodings
    face_person_db.datetime_updated = datetime.utcnow()

    db.commit()
    db.refresh(face_person_db)

    return schemas.FacePerson.from_orm(face_person_db)


async def delete_face_person(face_person_id: int, user: schemas.User, db: orm.Session):
    face_person_db = await _get_object_by_id(obj_id=face_person_id, user_id=user.id, model=models.FacePerson, db=db)

    db.delete(face_person_db)
    db.commit()


async def get_faces_images(user: schemas.User, db: orm.Session):
    faces_images = db.query(models.FaceImage).filter_by(owner_id=user.id)

    return list(map(schemas.FaceImage.from_orm, faces_images))


async def get_face_image(face_image_id: int, user: schemas.User, db: orm.Session):
    face_image_db = await _get_object_by_id(obj_id=face_image_id, user_id=user.id, model=models.FaceImage, db=db)

    return schemas.FaceImage.from_orm(face_image_db)


async def create_face_image(
    user: schemas.User, db: orm.Session, face_image: schemas.FaceImageCreate
):
    face_image = models.FaceImage(**face_image.dict(), owner_id=user.id)

    db.add(face_image)
    db.commit()
    db.refresh(face_image)
    return schemas.FaceImage.from_orm(face_image)


async def update_face_image(
    face_image_id: int, face_image: schemas.FaceImageCreate, user: schemas.User, db: orm.Session
):
    face_image_db = await _get_object_by_id(obj_id=face_image_id, user_id=user.id, model=models.FaceImage, db=db)

    face_image_db.name = face_image.name
    face_image_db.person_names = face_image.person_names
    face_image_db.face_locations = face_image.face_locations
    face_image_db.face_encodings = face_image.face_encodings
    face_image_db.datetime_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(face_image_db)

    return schemas.FaceImage.from_orm(face_image_db)


async def delete_face_image(face_image_id: int, user: schemas.User, db: orm.Session):
    face_image_db = await _get_object_by_id(obj_id=face_image_id, user_id=user.id, model=models.FaceImage, db=db)

    db.delete(face_image_db)
    db.commit()


async def create_match_faces(user: schemas.User, db: orm.Session):
    known_face_encodings = []
    known_face_names = []
    faces_persons = await get_faces_persons(user=user, db=db)
    for face_person in faces_persons:
        for encoding in face_person.face_encodings:
            known_face_encodings.append(encoding)
            known_face_names.append(face_person.name)
    faces_images = await get_faces_images(user=user, db=db)
    for face_image in faces_images:
        person_names = []
        for encoding in face_image.face_encodings:
            name = "Unknown"
            matches = face_recognition.compare_faces(np.array(known_face_encodings), np.array(encoding))
            face_distances = face_recognition.face_distance(np.array(known_face_encodings), np.array(encoding))
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            person_names.append(name)
        
        face_image.person_names = person_names
        face_image = await update_face_image(face_image_id=face_image.id, face_image=face_image, user=user, db=db)


async def get_match_faces(user: schemas.User, db: orm.Session):
    faces_image = db.query(models.FaceImage).filter_by(owner_id=user.id)
    images_person_names = {}
    for face_image in faces_image:
        if face_image.person_names:
            images_person_names[face_image.name] = [
                {   
                    'person_name': person_name,
                    'location': {'top': top, 'right': right, 'bottom': bottom, 'left': left}
                }
                for person_name, (top, right, bottom, left) in zip(face_image.person_names, face_image.face_locations)
            ]            

    return images_person_names


async def get_locations_and_encodings_from_image(image_base64: str):
    image = face_recognition.load_image_file(urlopen(image_base64))
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        raise fastapi.HTTPException(
            status_code=400, detail="Cannot recognize a face in the image."
        )

    face_encodings = face_recognition.face_encodings(image, face_locations)

    locations=list(map(list, face_locations))
    encodings=list(map(lambda e: e.tolist(), face_encodings))

    return locations, encodings


async def get_locations_and_encodings_from_images(images: list):
    locations, encodings = [], []
    for image_base64 in images:
        face_locations, face_encodings = await get_locations_and_encodings_from_image(image_base64)
        if len(face_locations) != 1:
            raise fastapi.HTTPException(
                status_code=400, detail="Must be only on face in the image."
            )
        locations.append(face_locations[0])
        encodings.append(face_encodings[0])

    return locations, encodings
