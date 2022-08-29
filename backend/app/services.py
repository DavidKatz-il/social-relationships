import io
import re
import json
import base64
import operator
import itertools
from typing import List
from datetime import datetime
from urllib.request import urlopen

import numpy as np
import networkx as nx
import fastapi
import jwt
import face_recognition
import matplotlib.pyplot as plt
from passlib.hash import bcrypt
from sqlalchemy import orm
from networkx.algorithms.community import louvain_communities
from PIL import Image, ImageDraw, ImageFont
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


async def validate_email(email: str, db: orm.Session):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not email or not re.match(email_regex, email):
        raise fastapi.HTTPException(status_code=400, detail="Invalid email address.")

    if await get_user_by_email(email=email, db=db):
        raise fastapi.HTTPException(status_code=400, detail="Email already exist.")


async def validate_hashed_password(hashed_password: str):
    min_pass_len = 6
    if len(hashed_password) < min_pass_len:
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"The password must contain at least {min_pass_len} characters.",
        )


async def validate_user(user: schemas.UserCreate, db: orm.Session):
    await validate_email(user.email, db)
    await validate_hashed_password(user.hashed_password)


async def create_user(user: schemas.UserCreate, db: orm.Session):
    await validate_user(user=user, db=db)

    user.hashed_password = bcrypt.hash(user.hashed_password)
    user_obj = models.User(**user.dict())

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def update_user(
    user_update: schemas.UserUpdate, user: schemas.User, db: orm.Session
):
    user_db = db.query(models.User).filter(models.User.id == user.id).first()

    if user_update.email and user_update.email != user_db.email:
        await validate_email(user_update.email, db=db)
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

    db.commit()
    db.refresh(user_db)

    return schemas.User.from_orm(user_db)


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
        raise fastapi.HTTPException(status_code=401, detail="Invalid Email or Password.")

    return schemas.User.from_orm(user)


async def _get_object_by_id(
    obj_id: int, user_id: int, model: database.Base, db: orm.Session
):
    obj_db = (
        db.query(model).filter_by(owner_id=user_id).filter(model.id == obj_id).first()
    )

    if obj_db is None:
        raise fastapi.HTTPException(status_code=404, detail="Object does not exist.")

    return obj_db


async def _get_object_by_name(
    obj_name: str, user_id: int, model: database.Base, db: orm.Session
):
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
    student_db = await _get_object_by_id(
        obj_id=student_id, user_id=user.id, model=models.Student, db=db
    )

    return schemas.Student.from_orm(student_db)


async def create_student(
    user: schemas.User, db: orm.Session, student: schemas.StudentCreate
):
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
    face_student = await create_face_student(
        user=user, db=db, face_student=face_student
    )

    return schemas.Student.from_orm(student)


async def update_student(
    student_id: int, student: schemas.StudentCreate, user: schemas.User, db: orm.Session
):
    student_db = await _get_object_by_id(
        obj_id=student_id, user_id=user.id, model=models.Student, db=db
    )
    face_student_db = await _get_object_by_name(
        obj_name=student_db.name, user_id=user.id, model=models.FaceStudent, db=db
    )

    if student.name != student_db.name:
        await validate_student_name_not_exist(
            student_name=student.name, user_id=user.id, db=db
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
        face_student_id=face_student_db.id, face_student=face_student, user=user, db=db
    )

    db.commit()
    db.refresh(student_db)

    return schemas.Student.from_orm(student_db)


async def delete_student(student_id: int, user: schemas.User, db: orm.Session):
    student_db = await _get_object_by_id(
        obj_id=student_id, user_id=user.id, model=models.Student, db=db
    )

    db.delete(student_db)
    db.commit()

    face_student_db = await _get_object_by_name(
        obj_name=student_db.name, user_id=user.id, model=models.FaceStudent, db=db
    )
    await delete_face_student(face_student_id=face_student_db.id, user=user, db=db)


async def validate_image(image: schemas.ImageCreate):
    if not image.name or not image.image:
        raise fastapi.HTTPException(
            status_code=400, detail="Image must have a name and a image."
        )


async def validate_image_name_not_exist(image_name: str, user_id: int, db: orm.Session):
    image_db = await _get_object_by_name(
        obj_name=image_name, user_id=user_id, model=models.Image, db=db
    )
    if image_db:
        raise fastapi.HTTPException(status_code=400, detail="Image already exist.")


async def get_images(user: schemas.User, db: orm.Session):
    images = db.query(models.Image).filter_by(owner_id=user.id)

    return list(map(schemas.Image.from_orm, images))


async def get_image(image_id: int, user: schemas.User, db: orm.Session):
    image_db = await _get_object_by_id(
        obj_id=image_id, user_id=user.id, model=models.Image, db=db
    )

    return schemas.Image.from_orm(image_db)


async def get_image_faces(image_id: int, user: schemas.User, db: orm.Session):
    image_db = await _get_object_by_id(
        obj_id=image_id, user_id=user.id, model=models.Image, db=db
    )
    face_db = (
        db.query(models.FaceImage)
        .filter_by(owner_id=user.id)
        .filter(models.FaceImage.name == image_db.name)
        .one_or_none()
    )
    if face_db:
        image_db.image = f"data:image/png;base64,{get_img_with_draw_boxes(image_db.image, face_db.face_locations, face_db.student_names)}"
    return schemas.Image.from_orm(image_db)


async def create_image(user: schemas.User, db: orm.Session, image: schemas.ImageCreate):
    await validate_image(image=image)
    await validate_image_name_not_exist(image_name=image.name, user_id=user.id, db=db)

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
    db.add(image)
    db.commit()
    db.refresh(image)

    face_image = await create_face_image(user=user, db=db, face_image=face_image)

    return schemas.Image.from_orm(image)


async def delete_image(image_id: int, user: schemas.User, db: orm.Session):
    image_db = await _get_object_by_id(
        obj_id=image_id, user_id=user.id, model=models.Image, db=db
    )

    db.delete(image_db)
    db.commit()

    face_image_db = await _get_object_by_name(
        obj_name=image_db.name, user_id=user.id, model=models.FaceImage, db=db
    )
    await delete_face_image(face_image_id=face_image_db.id, user=user, db=db)


async def get_faces_students(user: schemas.User, db: orm.Session):
    faces_students = db.query(models.FaceStudent).filter_by(owner_id=user.id)

    return list(map(schemas.FaceStudent.from_orm, faces_students))


async def get_face_student(face_student_id: int, user: schemas.User, db: orm.Session):
    face_student_db = await _get_object_by_id(
        obj_id=face_student_id, user_id=user.id, model=models.FaceStudent, db=db
    )

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
    face_student_id: int,
    face_student: schemas.FaceStudentCreate,
    user: schemas.User,
    db: orm.Session,
):
    face_student_db = await _get_object_by_id(
        obj_id=face_student_id, user_id=user.id, model=models.FaceStudent, db=db
    )

    face_student_db.name = face_student.name
    face_student_db.face_locations = face_student.face_locations
    face_student_db.face_encodings = face_student.face_encodings
    face_student_db.datetime_updated = datetime.utcnow()

    db.commit()
    db.refresh(face_student_db)

    return schemas.FaceStudent.from_orm(face_student_db)


async def delete_face_student(
    face_student_id: int, user: schemas.User, db: orm.Session
):
    face_student_db = await _get_object_by_id(
        obj_id=face_student_id, user_id=user.id, model=models.FaceStudent, db=db
    )

    db.delete(face_student_db)
    db.commit()


async def get_faces_images(user: schemas.User, db: orm.Session):
    faces_images = db.query(models.FaceImage).filter_by(owner_id=user.id)

    return list(map(schemas.FaceImage.from_orm, faces_images))


async def get_face_image(face_image_id: int, user: schemas.User, db: orm.Session):
    face_image_db = await _get_object_by_id(
        obj_id=face_image_id, user_id=user.id, model=models.FaceImage, db=db
    )

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
    face_image_id: int,
    face_image: schemas.FaceImageCreate,
    user: schemas.User,
    db: orm.Session,
):
    face_image_db = await _get_object_by_id(
        obj_id=face_image_id, user_id=user.id, model=models.FaceImage, db=db
    )

    face_image_db.name = face_image.name
    face_image_db.student_names = face_image.student_names
    face_image_db.face_locations = face_image.face_locations
    face_image_db.face_encodings = face_image.face_encodings
    face_image_db.datetime_updated = datetime.utcnow()

    db.commit()
    db.refresh(face_image_db)

    return schemas.FaceImage.from_orm(face_image_db)


async def delete_face_image(face_image_id: int, user: schemas.User, db: orm.Session):
    face_image_db = await _get_object_by_id(
        obj_id=face_image_id, user_id=user.id, model=models.FaceImage, db=db
    )

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
            face_image_id=face_image.id, face_image=face_image, user=user, db=db
        )


async def get_match_faces(user: schemas.User, db: orm.Session):
    faces_image = db.query(models.FaceImage).filter_by(owner_id=user.id)
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
    user: schemas.User, db: orm.Session, exclude_unknown: bool = True
):
    faces_image = db.query(models.FaceImage).filter_by(owner_id=user.id)
    student_list = await get_students_list(user, db, exclude_unknown)
    images_by_name = {name: [] for name in student_list}
    for face_image in faces_image:
        if face_image.student_names:
            for stdnt_name in face_image.student_names:
                if exclude_unknown and stdnt_name == "Unknown":
                    continue
                images_by_name[stdnt_name].append(face_image.name)

    return images_by_name


async def get_match_faces_by_image(
    user: schemas.User, db: orm.Session, exclude_unknown: bool = True
):
    faces_image = db.query(models.FaceImage).filter_by(owner_id=user.id)
    images_by_name = {}
    for face_image in faces_image:
        if face_image.student_names:
            if exclude_unknown and "Unknown" in face_image.student_names:
                face_image.student_names.remove("Unknown")
            images_by_name[face_image.name] = list(face_image.student_names)

    return images_by_name


async def get_locations_and_encodings_from_image(image_base64: str):
    def get_locations(image):
        locations = face_recognition.face_locations(
            image, number_of_times_to_upsample=1, model="hog"
        )
        if len(locations) == 0:
            locations = face_recognition.face_locations(
                image, number_of_times_to_upsample=2, model="cnn"
            )
        return locations

    image = face_recognition.load_image_file(urlopen(image_base64))
    face_locations = get_locations(image)
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
        face_locations, face_encodings = await get_locations_and_encodings_from_image(
            image_base64
        )
        if len(face_locations) != 1:
            raise fastapi.HTTPException(
                status_code=400, detail="Must be only on face in the image."
            )
        locations.append(face_locations[0])
        encodings.append(face_encodings[0])

    return locations, encodings


async def get_students_list(
    user: schemas.User, db: orm.Session, exclude_unknown: bool = True
) -> list:
    name_list = []
    for lst_info in (await get_match_faces(user, db)).values():
        for dict_info in lst_info:
            if exclude_unknown and dict_info["student_name"] == "Unknown":
                continue
            name_list.append(dict_info["student_name"])
    return name_list


async def validate_report_not_exist(report_name: str, user_id: int, db: orm.Session):
    report_db = await _get_object_by_name(
        obj_name=report_name, user_id=user_id, model=models.Report, db=db
    )
    if report_db:
        raise fastapi.HTTPException(status_code=400, detail="Report already exist.")


async def create_report1(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    stdnt_list_by_name = await get_match_faces_by_student(user, db)
    report_table_header = ["Student", "Count", "Images"]
    if not stdnt_list_by_name:
        return {0: report_table_header}

    total_appear = {
        0: report_table_header,
        **{
            i: [
                name,
                len(stdnt_list_by_name[name]),
                ", ".join(sorted(stdnt_list_by_name[name])),
            ]
            for i, name in enumerate(stdnt_list_by_name, start=1)
        },
    }

    return total_appear


async def create_report2(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    name_list = await get_students_list(user, db)
    report_table_header = ["Student", "Count"]
    if not name_list:
        return {0: report_table_header}

    total_count = {name: name_list.count(name) for name in name_list}
    max_count = max(total_count.values())
    names_most_appear = [
        name for name, count in total_count.items() if count == max_count
    ]

    most_popular_student = {
        0: report_table_header,
        **{
            i: [name, max_count]
            for i, name in enumerate(sorted(names_most_appear), start=1)
        },
    }

    return most_popular_student


async def create_report3(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    name_list = await get_students_list(user, db)
    report_table_header = ["Student", "BFF", "Count"]
    if not name_list:
        return {0: report_table_header}

    stdnt_list_by_name = await get_match_faces_by_student(user, db)

    besties = {stndt_name: {} for stndt_name in name_list}
    for nested_stndt_name in besties:
        besties[nested_stndt_name] = {
            name: 0 for name in name_list if name != nested_stndt_name
        }

    for stdnt in stdnt_list_by_name:
        for nested_stdnt in stdnt_list_by_name:
            if stdnt == nested_stdnt:
                continue
            match_pic = list(
                set(stdnt_list_by_name[stdnt]).intersection(
                    stdnt_list_by_name[nested_stdnt]
                )
            )
            if len(match_pic) > 0:
                besties[stdnt][nested_stdnt] = len(match_pic)

    besties_counter = {
        0: report_table_header,
        **{
            i: [name, *max(besties[name].items(), key=operator.itemgetter(1))]
            for i, name in enumerate(sorted(set(besties)), start=1)
        },
    }

    return besties_counter


async def create_report4(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    stdnt_list_by_name = await get_match_faces_by_student(
        user, db, exclude_unknown=False
    )

    report_table_header = ["Image", "Count"]
    if not stdnt_list_by_name:
        return {0: report_table_header}

    total_appear = {
        0: report_table_header,
        **{
            i: [image_name, stdnt_list_by_name["Unknown"].count(image_name)]
            for i, image_name in enumerate(
                sorted(set(stdnt_list_by_name["Unknown"])), start=1
            )
        },
    }

    return total_appear


async def create_report5(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    image_list_by_student = await get_match_faces_by_image(user, db)
    edgelist = [
        tuple(pair)
        for studens in image_list_by_student.values()
        for pair in itertools.combinations(studens, 2)
    ]

    report_table_header = ["Community", "Members"]
    if not edgelist:
        return {0: report_table_header}

    G = nx.from_edgelist(edgelist)

    communities = sorted(map(sorted, louvain_communities(G)))
    communities_report = {
        0: report_table_header,
        **{
            i: [f"{i}", ", ".join(community)]
            for i, community in enumerate(communities, start=1)
        },
    }

    return communities_report


async def create_report6(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    def get_graph_draw_str(graph):
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos=pos, with_labels=True, node_color="skyblue", font_size=8)
        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=nx.get_edge_attributes(graph, "weight"),
            rotate=False,
            font_size=8,
        )
        s = io.BytesIO()
        plt.savefig(s, format="png", bbox_inches="tight")
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        plt.close()
        return s

    if recreate_match_faces:
        await create_match_faces(user, db)

    image_list_by_student = await get_match_faces_by_image(user, db)

    if not image_list_by_student:
        return {"images": []}

    edgelist = [
        tuple(pair)
        for studens in image_list_by_student.values()
        for pair in itertools.combinations(studens, 2)
    ]
    all_students = [
        student.name
        for student in db.query(models.Student)
        .filter_by(owner_id=user.id)
        .with_entities(models.Student.name)
        .distinct()
        .all()
    ]

    G = nx.from_edgelist(edgelist)
    graph_draw_images = [get_graph_draw_str(G)]
    if sorted(G.nodes) != sorted(all_students):
        G.add_nodes_from(all_students)
        graph_draw_images.append(get_graph_draw_str(G))

    graph_draw_report = {
        "images": [
            f"data:image/png;base64,{base64_str}" for base64_str in graph_draw_images
        ],
    }

    return graph_draw_report


async def create_report7(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    name_list = await get_students_list(user, db)

    report_table_header = ["Student", "Count", "Students"]
    if not name_list:
        return {0: report_table_header}

    stdnt_list_by_name = await get_match_faces_by_student(user, db)

    my_friends = {stndt_name: {} for stndt_name in name_list}
    for nested_stndt_name in my_friends:
        my_friends[nested_stndt_name] = {
            name: 0 for name in name_list if name != nested_stndt_name
        }

    for stdnt in stdnt_list_by_name:
        for nested_stdnt in stdnt_list_by_name:
            if stdnt == nested_stdnt:
                continue
            match_pic = list(
                set(stdnt_list_by_name[stdnt]).intersection(
                    stdnt_list_by_name[nested_stdnt]
                )
            )
            if len(match_pic) > 0:
                my_friends[stdnt][nested_stdnt] = len(match_pic)

    student_group = {}

    for stdnt_name in my_friends.keys():
        student_group[stdnt_name] = []
        for friend in my_friends[stdnt_name]:
            if my_friends[stdnt_name][friend] > 0:
                student_group[stdnt_name].append(friend)

    student_group_cnt_report = {
        0: report_table_header,
        **{
            i: [name, len(student_group[name]), ", ".join(sorted(student_group[name]))]
            for i, name in enumerate(sorted(set(student_group)), start=1)
        },
    }

    return student_group_cnt_report


async def create_report8(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    students_in_images = await get_students_list(user, db)
    report_table_header = ["Student"]
    if not report_table_header:
        return {0: report_table_header}

    all_students = (
        db.query(models.Student)
        .filter_by(owner_id=user.id)
        .with_entities(models.Student.name)
        .distinct()
        .all()
    )
    missing_students = set([student_name for student_name, in all_students]) - set(
        students_in_images
    )
    not_appear_report = {
        0: report_table_header,
        **{i: [name] for i, name in enumerate(sorted(missing_students), start=1)},
    }

    return not_appear_report


async def create_report9(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    image_list_by_student = await get_match_faces_by_image(
        user, db, exclude_unknown=False
    )

    report_table_header = ["Image", "Count", "Students"]
    if not image_list_by_student:
        return {0: report_table_header}

    image_students_report = {
        0: report_table_header,
        **{
            i: [
                image_name,
                len(image_list_by_student[image_name]),
                ", ".join(image_list_by_student[image_name]),
            ]
            for i, image_name in enumerate(sorted(image_list_by_student), start=1)
        },
    }

    return image_students_report


def get_img_with_draw_boxes(
    image_data: str, locations: List[List[int]], names: List[str]
):
    image_data = re.sub("^data:image/.+;base64,", "", image_data)
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    draw = ImageDraw.Draw(image)

    for (top, right, bottom, left), student_name in zip(locations, names):
        student_name = student_name.encode("utf-8")
        text_width, text_height = draw.textsize(student_name)
        text_width, text_height = text_width * 5, text_height * 5

        color = (0, 0, 255)
        if student_name == b"Unknown":
            color = (255, 0, 0)

        draw.rectangle(((left, top), (right, bottom)), outline=color)
        draw.rectangle(
            ((left, bottom), (right, bottom + int(image.size[0] * 0.02))),
            fill=color,
            outline=color,
        )

        font = ImageFont.truetype("./data/arial.ttf", int(image.size[0] * 0.015))
        draw.text(
            (left, bottom),
            student_name.decode("utf-8"),
            fill=(255, 255, 255, 255),
            font=font,
        )

    buffered = io.BytesIO()
    image.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8").replace("\n", "")
    image.close()
    return img_str


async def create_report10(
    user: schemas.User, db: orm.Session, recreate_match_faces: bool = True
):
    if recreate_match_faces:
        await create_match_faces(user, db)

    db_images = db.query(models.Image).filter_by(owner_id=user.id).all()
    if not db_images:
        return {"images": []}

    images = {}
    for image_db in db_images:
        face_db = (
            db.query(models.FaceImage)
            .filter_by(owner_id=user.id)
            .filter(models.FaceImage.name == image_db.name)
            .one()
        )
        images[image_db.name] = get_img_with_draw_boxes(
            image_db.image, face_db.face_locations, face_db.student_names
        )

    images_report = {
        "images": [
            f"data:image/png;base64,{images[image_name]}"
            for image_name in sorted(images)
        ],
    }

    return images_report


async def save_report_in_db(
    name_of_report,
    report_info,
    user: schemas.User,
    db: orm.Session,
):
    report = schemas.ReportCreate(
        name=name_of_report,
        info=report_info,
    )
    report = models.Report(**report.dict(), owner_id=user.id)
    db.add(report)
    db.commit()
    db.refresh(report)


async def create_reports(user: schemas.User, db: orm.Session):
    if (db.query(models.Image).filter_by(owner_id=user.id).count() == 0) or (
        db.query(models.Student).filter_by(owner_id=user.id).count() == 0
    ):
        raise fastapi.HTTPException(
            status_code=400, detail="There must be at least one student and one image."
        )

    await create_match_faces(user, db)

    reports_creators = {
        "Total appear": create_report1,
        "Most appearance": create_report2,
        "Besties": create_report3,
        "Images with unknown": create_report4,
        "Communities": create_report5,
        "Graph": create_report6,
        "Friends": create_report7,
        "Not appear": create_report8,
        "Who is in the image": create_report9,
        "Images": create_report10,
    }
    for report_name, report_creator in reports_creators.items():
        await validate_report_not_exist(report_name=report_name, user_id=user.id, db=db)
        report = await report_creator(user, db, recreate_match_faces=False)
        await save_report_in_db(report_name, report, user, db)

    return {"message", "Successfully finished reports creating."}


async def update_reports(user: schemas.User, db: orm.Session):
    await create_match_faces(user, db)

    for report in await get_reports_info(user, db):
        await update_report(report.id, user, db, recreate_match_faces=False)

    return {"message", "Successfully finished reports updates."}


async def get_reports(user: schemas.User, db: orm.Session):
    report = db.query(models.Report).filter_by(owner_id=user.id)

    return list(map(schemas.Report.from_orm, report))


async def get_specific_report(
    user: schemas.User, db: orm.Session, report_id: schemas.Report
):
    report_db = await _get_object_by_id(
        obj_id=report_id, user_id=user.id, model=models.Report, db=db
    )

    return schemas.Report.from_orm(report_db)


async def delete_report(report_id: int, user: schemas.User, db: orm.Session):
    report_db = await _get_object_by_id(
        obj_id=report_id, user_id=user.id, model=models.Report, db=db
    )

    db.delete(report_db)
    db.commit()


async def update_report(
    report_id: int,
    user: schemas.User,
    db: orm.Session,
    recreate_match_faces: bool = True,
):
    report_db = await _get_object_by_id(
        obj_id=report_id, user_id=user.id, model=models.Report, db=db
    )

    report_creator = {
        "Total appear": create_report1,
        "Most appearance": create_report2,
        "Besties": create_report3,
        "Images with unknown": create_report4,
        "Communities": create_report5,
        "Graph": create_report6,
        "Friends": create_report7,
        "Not appear": create_report8,
        "Who is in the image": create_report9,
        "Images": create_report10,
    }

    report_db.info = await report_creator[report_db.name](
        user, db, recreate_match_faces
    )
    report_db.datetime_updated = datetime.utcnow()

    db.commit()
    db.refresh(report_db)

    return schemas.Report.from_orm(report_db)


async def get_reports_info(user: schemas.User, db: orm.Session):
    reports = (
        db.query(models.Report)
        .filter_by(owner_id=user.id)
        .with_entities(models.Report.id, models.Report.name)
    )
    return list(map(schemas.ReportInfo.from_orm, reports))


async def get_user_info(user: schemas.User, db: orm.Session):
    students_count = db.query(models.Student).filter_by(owner_id=user.id).count()
    images_count = db.query(models.Image).filter_by(owner_id=user.id).count()
    user_info = {"students_count": students_count, "images_count": images_count}
    return schemas.UserInfo(**user_info)
