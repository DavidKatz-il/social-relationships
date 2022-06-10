import json
import operator
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


async def validate_student(student: schemas.StudentCreate):
    if not student.name or not student.images or (student.images == "[]"):
        raise fastapi.HTTPException(
            status_code=400, detail="Student must have a name and at least one image."
        )


async def validate_student_name_not_exist(
        student_name: str, user_id: int, db: orm.Session
):
    student_db = await _get_object_by_name(
        obj_name=student_name, user_id=user_id, model=models.Student, db=db
    )
    if student_db:
        raise fastapi.HTTPException(status_code=400, detail="Student already exist.")


async def get_students(user: schemas.User, db: orm.Session):
    students = db.query(models.Student).filter_by(owner_id=user.id)

    return list(map(schemas.Student.from_orm, students))


async def get_student(student_id: int, user: schemas.User, db: orm.Session):
    student_db = await _get_object_by_id(obj_id=student_id, user_id=user.id, model=models.Student, db=db)

    return schemas.Student.from_orm(student_db)


async def create_student(
        user: schemas.User, db: orm.Session, student: schemas.StudentCreate
):
    await validate_student(student=student)
    await validate_student_name_not_exist(
        student_name=student.name, user_id=user.id, db=db
    )

    locations, encodings = await get_locations_and_encodings_from_images(
        images=json.loads(student.images)
    )
    face_student = schemas.FaceStudentCreate(
        face_locations=locations, face_encodings=encodings, name=student.name
    )

    student = models.Student(**student.dict(), owner_id=user.id)
    db.add(student)
    db.commit()
    db.refresh(student)
    face_student = await create_face_student(user=user, db=db, face_student=face_student)

    return schemas.Student.from_orm(student)


async def update_student(
        student_id: int, student: schemas.StudentCreate, user: schemas.User, db: orm.Session
):
    student_db = await _get_object_by_id(obj_id=student_id, user_id=user.id, model=models.Student, db=db)
    if student.name != student_db.name:
        await validate_student_name_not_exist(
            student_name=student.name, user_id=user.id, db=db
        )

    student_db.name = student.name
    student_db.images = student.images
    student_db.datetime_updated = datetime.utcnow()

    await validate_student(student=student_db)
    locations, encodings = await get_locations_and_encodings_from_images(
        images=json.loads(student.images)
    )
    face_student = schemas.FaceStudentCreate(
        face_locations=locations, face_encodings=encodings, name=student.name
    )
    face_student_db = await _get_object_by_name(obj_name=student_db.name, user_id=user.id, model=models.FaceStudent,
                                                db=db)
    face_student = await update_face_student(face_student_id=face_student_db.id, face_student=face_student, user=user,
                                             db=db)

    db.commit()
    db.refresh(student_db)

    return schemas.Student.from_orm(student_db)


async def delete_student(student_id: int, user: schemas.User, db: orm.Session):
    student_db = await _get_object_by_id(obj_id=student_id, user_id=user.id, model=models.Student, db=db)

    db.delete(student_db)
    db.commit()

    face_student_db = await _get_object_by_name(obj_name=student_db.name, user_id=user.id, model=models.FaceStudent,
                                                db=db)
    await delete_face_student(face_student_id=face_student_db.id, user=user, db=db)


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
        face_locations=locations, face_encodings=encodings, name=image.name, student_names=[]
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


async def get_faces_students(user: schemas.User, db: orm.Session):
    faces_students = db.query(models.FaceStudent).filter_by(owner_id=user.id)

    return list(map(schemas.FaceStudent.from_orm, faces_students))


async def get_face_student(face_student_id: int, user: schemas.User, db: orm.Session):
    face_student_db = await _get_object_by_id(obj_id=face_student_id, user_id=user.id, model=models.FaceStudent, db=db)

    return schemas.FaceStudent.from_orm(face_student_db)


async def create_face_student(
        user: schemas.User, db: orm.Session, face_student: schemas.FaceStudentCreate
):
    face_student = models.FaceStudent(**face_student.dict(), owner_id=user.id)

    db.add(face_student)
    db.commit()
    db.refresh(face_student)
    return schemas.FaceStudent.from_orm(face_student)


async def update_face_student(
        face_student_id: int, face_student: schemas.FaceStudentCreate, user: schemas.User, db: orm.Session
):
    face_student_db = await _get_object_by_id(obj_id=face_student_id, user_id=user.id, model=models.FaceStudent, db=db)

    face_student_db.name = face_student.name
    face_student_db.face_locations = face_student.face_locations
    face_student_db.face_encodings = face_student.face_encodings
    face_student_db.datetime_updated = datetime.utcnow()

    db.commit()
    db.refresh(face_student_db)

    return schemas.FaceStudent.from_orm(face_student_db)


async def delete_face_student(face_student_id: int, user: schemas.User, db: orm.Session):
    face_student_db = await _get_object_by_id(obj_id=face_student_id, user_id=user.id, model=models.FaceStudent, db=db)

    db.delete(face_student_db)
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
    face_image_db.student_names = face_image.student_names
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
    faces_students = await get_faces_students(user=user, db=db)
    for face_student in faces_students:
        for encoding in face_student.face_encodings:
            known_face_encodings.append(encoding)
            known_face_names.append(face_student.name)
    faces_images = await get_faces_images(user=user, db=db)
    for face_image in faces_images:
        student_names = []
        for encoding in face_image.face_encodings:
            name = "Unknown"
            matches = face_recognition.compare_faces(np.array(known_face_encodings), np.array(encoding))
            face_distances = face_recognition.face_distance(np.array(known_face_encodings), np.array(encoding))
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            student_names.append(name)

        face_image.student_names = student_names
        face_image = await update_face_image(face_image_id=face_image.id, face_image=face_image, user=user, db=db)


async def get_match_faces(user: schemas.User, db: orm.Session):
    faces_image = db.query(models.FaceImage).filter_by(owner_id=user.id)
    images_student_names = {}
    for face_image in faces_image:
        if face_image.student_names:
            images_student_names[face_image.name] = [
                {
                    'student_name': student_name,
                    'location': {'top': top, 'right': right, 'bottom': bottom, 'left': left}
                }
                for student_name, (top, right, bottom, left) in zip(face_image.student_names, face_image.face_locations)
            ]

    return images_student_names


async def get_match_faces_by_student(user: schemas.User, db: orm.Session):
    faces_image = db.query(models.FaceImage).filter_by(owner_id=user.id)
    student_list = await get_students_list(user, db)
    images_by_name = {name: [] for name in student_list}
    for face_image in faces_image:
        if face_image.student_names:
            for stdnt_name in face_image.student_names:
                images_by_name[stdnt_name].append(face_image.name)

    return images_by_name


async def get_locations_and_encodings_from_image(image_base64: str):
    image = face_recognition.load_image_file(urlopen(image_base64))
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        raise fastapi.HTTPException(
            status_code=400, detail="Cannot recognize a face in the image."
        )

    face_encodings = face_recognition.face_encodings(image, face_locations)

    locations = list(map(list, face_locations))
    encodings = list(map(lambda e: e.tolist(), face_encodings))

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


async def get_students_list(user: schemas.User, db: orm.Session) -> list:
    name_list = []
    for lst_info in (await get_match_faces(user, db)).values():
        for dict_info in lst_info:
            name_list.append(dict_info["student_name"])
    return name_list


async def validate_report_not_exist(
        report_name: str,
        user_id: int,
        db: orm.Session
):
    report_db = await _get_object_by_name(
        obj_name=report_name,
        user_id=user_id,
        model=models.Report,
        db=db
    )
    if report_db:
        raise fastapi.HTTPException(status_code=400, detail="Report already exist.")


async def create_reports(
        user: schemas.User,
        db: orm.Session,
):
    name_of_report1 = "Total appear"

    await validate_report_not_exist(
        report_name=name_of_report1,
        user_id=user.id,
        db=db
    )

    await create_match_faces(user, db)
    name_list = await get_students_list(user, db)
    total_appear = {
        0: ['name', 'count'],
        **{
            i + 1: [name, name_list.count(name)]
            for i, name in enumerate(set(name_list))
        }
    }

    rprt = schemas.Report(
        name=name_of_report1, info=total_appear,
    )
    a = models.Report(**rprt.dict(), owner_id=user.id)
    db.add(a)
    db.commit()
    db.refresh(a)

    return [schemas.Report.from_orm(rprt)]


async def get_reports(user: schemas.User, db: orm.Session):
    report = db.query(models.Report).filter_by(owner_id=user.id)

    return list(map(schemas.Report.from_orm, report))


async def get_report(
        user: schemas.User,
        db: orm.Session,
        report_id: schemas.Report
):
    report_db = await _get_object_by_id(obj_id=report_id, user_id=user.id, model=models.Report, db=db)

    return schemas.Report.from_orm(report_db)


# await create_match_faces(user, db)
# name_list = await get_students_list(user, db)
#
# total_appear = {
#     0: ['name', 'count'],
#     **{
#         i + 1: [name, name_list.count(name)]
#         for i, name in enumerate(set(name_list))
#     }
# }
#
# total_count = {name: name_list.count(name) for name in name_list}
# most_apper = max(total_count, key=total_count.get)
#
# stdnt_list_by_name = await get_match_faces_by_student(user, db)
#
# besties = {stndt_name: {} for stndt_name in name_list}
# for nested_stndt_name in besties:
#     besties[nested_stndt_name] = {name: 0 for name in name_list if name != nested_stndt_name}
#
# for stdnt in stdnt_list_by_name:
#     for nesten_stdnt in stdnt_list_by_name:
#         if stdnt == nesten_stdnt:
#             continue
#         match_pic = \
#             list(set(stdnt_list_by_name[stdnt]).intersection(stdnt_list_by_name[nesten_stdnt]))
#         besties[stdnt][nesten_stdnt] = len(match_pic)
# try:
#     del besties['Unknown']
# except KeyError:
#     pass
#
# besties_counter = {
#     0: ['name', 'besties', 'count'],
#     **{
#         i + 1: [name, *max(besties[name].items(), key=operator.itemgetter(1))]
#         for i, name in enumerate(set(besties))
#     }
# }
#
# rprt = models.Report(besties_counter, owner_id=user.id)
#
# return [besties_counter]

# return [
# {
#     # "name": "Total appearance",
#     # "info": f"{total_appear}",
#     "id": 0,
#     "datetime_created": "2022-05-22T21:05:00.799Z",
#     "datetime_updated": "2022-05-22T21:05:00.799Z"
# },
# {
#     "report_id": 1,
#     "name": "Most appearance",
#     "info": f"{most_apper}: {total_count[most_apper]}",
#     "datetime_created": "2022-05-22T21:05:00.799Z",
#     "datetime_updated": "2022-05-22T21:05:00.799Z"
# },
# {
#     "report_id": 2,
#     "name": "Most appearance",
#     "info": f"{besties_counter}",
#     "datetime_created": "2022-05-22T21:05:00.799Z",
#     "datetime_updated": "2022-05-22T21:05:00.799Z"
# }
# ]


'''
report_closet_friends = {
  0: ["student name", "closet friends"],
  1: ["yakkov dayan", "haim hugi"],
   ...
}
'''
