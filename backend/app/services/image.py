from datetime import datetime

from sqlalchemy import orm

from app import models, schemas
from app.core_utils.face_recognition import get_locations_and_encodings_from_image
from app.core_utils.image import draw_face_boxes
from app.services.utils.db import get_object_by_id, get_object_by_name
from app.services.utils.validations import validate_image, validate_image_name_not_exist


async def get_images(user: schemas.User, db_session: orm.Session):
    images = db_session.query(models.Image).filter_by(owner_id=user.id)

    return list(map(schemas.Image.from_orm, images))


async def get_image(image_id: int, user: schemas.User, db_session: orm.Session):
    image_db = await get_object_by_id(
        obj_id=image_id, user_id=user.id, model=models.Image, db_session=db_session
    )

    return schemas.Image.from_orm(image_db)


async def get_image_faces(image_id: int, user: schemas.User, db_session: orm.Session):
    image_db = await get_object_by_id(
        obj_id=image_id, user_id=user.id, model=models.Image, db_session=db_session
    )
    face_db = (
        db_session.query(models.FaceImage)
        .filter_by(owner_id=user.id)
        .filter(models.FaceImage.name == image_db.name)
        .one_or_none()
    )
    if face_db:
        image_db.image = draw_face_boxes(
            image_db.image, face_db.student_names, face_db.face_locations
        )
    return schemas.Image.from_orm(image_db)


async def create_image(
    user: schemas.User, db_session: orm.Session, image: schemas.ImageCreate
):
    await validate_image(image=image)
    await validate_image_name_not_exist(
        image_name=image.name, user_id=user.id, db_session=db_session
    )

    locations, encodings = await get_locations_and_encodings_from_image(
        image_base64=image.image
    )
    face_image = schemas.FaceImageCreate(
        face_locations=locations,
        face_encodings=encodings,
        name=image.name,
        student_names=[],
    )

    image = models.Image(**image.dict(), owner_id=user.id)
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)

    face_image = await create_face_image(
        user=user, db_session=db_session, face_image=face_image
    )

    return schemas.Image.from_orm(image)


async def delete_image(image_id: int, user: schemas.User, db_session: orm.Session):
    image_db = await get_object_by_id(
        obj_id=image_id, user_id=user.id, model=models.Image, db_session=db_session
    )

    db_session.delete(image_db)
    db_session.commit()

    face_image_db = await get_object_by_name(
        obj_name=image_db.name,
        user_id=user.id,
        model=models.FaceImage,
        db_session=db_session,
    )
    await delete_face_image(
        face_image_id=face_image_db.id, user=user, db_session=db_session
    )


async def get_faces_images(user: schemas.User, db_session: orm.Session):
    faces_images = db_session.query(models.FaceImage).filter_by(owner_id=user.id)

    return list(map(schemas.FaceImage.from_orm, faces_images))


async def get_face_image(
    face_image_id: int, user: schemas.User, db_session: orm.Session
):
    face_image_db = await get_object_by_id(
        obj_id=face_image_id,
        user_id=user.id,
        model=models.FaceImage,
        db_session=db_session,
    )

    return schemas.FaceImage.from_orm(face_image_db)


async def create_face_image(
    user: schemas.User, db_session: orm.Session, face_image: schemas.FaceImageCreate
):
    face_image = models.FaceImage(**face_image.dict(), owner_id=user.id)

    db_session.add(face_image)
    db_session.commit()
    db_session.refresh(face_image)
    return schemas.FaceImage.from_orm(face_image)


async def update_face_image(
    face_image_id: int,
    face_image: schemas.FaceImageCreate,
    user: schemas.User,
    db_session: orm.Session,
):
    face_image_db = await get_object_by_id(
        obj_id=face_image_id,
        user_id=user.id,
        model=models.FaceImage,
        db_session=db_session,
    )

    face_image_db.name = face_image.name
    face_image_db.student_names = face_image.student_names
    face_image_db.face_locations = face_image.face_locations
    face_image_db.face_encodings = face_image.face_encodings
    face_image_db.datetime_updated = datetime.utcnow()

    db_session.commit()
    db_session.refresh(face_image_db)

    return schemas.FaceImage.from_orm(face_image_db)


async def delete_face_image(
    face_image_id: int, user: schemas.User, db_session: orm.Session
):
    face_image_db = await get_object_by_id(
        obj_id=face_image_id,
        user_id=user.id,
        model=models.FaceImage,
        db_session=db_session,
    )

    db_session.delete(face_image_db)
    db_session.commit()
