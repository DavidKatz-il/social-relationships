from typing import List

import face_recognition
import fastapi
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import orm

from app import models, schemas
from app.services.image import get_faces_images, update_face_image
from app.services.student import get_faces_students


async def create_match_faces(user: schemas.User, db_session: orm.Session):
    known_face_encodings = []
    known_face_names = []
    faces_students = await get_faces_students(user=user, db_session=db_session)
    for face_student in faces_students:
        for encoding in face_student.face_encodings:
            known_face_encodings.append(encoding)
            known_face_names.append(face_student.name)
    faces_images = await get_faces_images(user=user, db_session=db_session)
    for face_image in faces_images:
        student_names = []
        for encoding in face_image.face_encodings:
            name = "Unknown"
            matches = face_recognition.compare_faces(
                np.array(known_face_encodings), np.array(encoding)
            )
            face_distances = face_recognition.face_distance(
                np.array(known_face_encodings), np.array(encoding)
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            student_names.append(name)

        face_image.student_names = student_names
        face_image = await update_face_image(
            face_image_id=face_image.id,
            face_image=face_image,
            user=user,
            db_session=db_session,
        )


async def get_match_faces(user: schemas.User, db_session: orm.Session):
    faces_image = db_session.query(models.FaceImage).filter_by(owner_id=user.id)
    images_student_names = {}
    for face_image in faces_image:
        if face_image.student_names:
            images_student_names[face_image.name] = [
                {
                    "student_name": student_name,
                    "location": {
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                        "left": left,
                    },
                }
                for student_name, (top, right, bottom, left) in zip(
                    face_image.student_names, face_image.face_locations
                )
            ]

    return images_student_names


async def get_match_faces_by_student(
    user: schemas.User, db_session: orm.Session, exclude_unknown: bool = True
):
    faces_image = db_session.query(models.FaceImage).filter_by(owner_id=user.id)
    student_list = await get_students_list(user, db_session, exclude_unknown)
    images_by_name = {name: [] for name in student_list}
    for face_image in faces_image:
        if face_image.student_names:
            for stdnt_name in face_image.student_names:
                if exclude_unknown and stdnt_name == "Unknown":
                    continue
                images_by_name[stdnt_name].append(face_image.name)

    return images_by_name


async def get_match_faces_by_image(
    user: schemas.User, db_session: orm.Session, exclude_unknown: bool = True
):
    faces_image = db_session.query(models.FaceImage).filter_by(owner_id=user.id)
    images_by_name = {}
    for face_image in faces_image:
        if face_image.student_names:
            if exclude_unknown and "Unknown" in face_image.student_names:
                face_image.student_names.remove("Unknown")
            images_by_name[face_image.name] = list(face_image.student_names)

    return images_by_name


async def get_students_list(
    user: schemas.User, db_session: orm.Session, exclude_unknown: bool = True
) -> list:
    name_list = []
    for lst_info in (await get_match_faces(user, db_session)).values():
        for dict_info in lst_info:
            if exclude_unknown and dict_info["student_name"] == "Unknown":
                continue
            name_list.append(dict_info["student_name"])
    return name_list


async def get_images(user: schemas.User, db_session: orm.Session) -> list:
    db_images = db_session.query(models.Image).filter_by(owner_id=user.id).all()
    if not db_images:
        return []

    images = []
    for image_db in db_images:
        face_db = (
            db_session.query(models.FaceImage)
            .filter_by(owner_id=user.id)
            .filter(models.FaceImage.name == image_db.name)
            .one()
        )
        images.append(
            {
                "image": image_db.image,
                "student_names": face_db.student_names,
                "face_locations": face_db.face_locations,
            }
        )

    return images
