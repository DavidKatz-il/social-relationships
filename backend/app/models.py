from datetime import datetime

import sqlalchemy as sql
from passlib.hash import bcrypt

from app import database


USERS_ID = "users.id"


class User(database.Base):
    __tablename__ = "users"
    
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    teacher_name = sql.Column(sql.String)
    school_name = sql.Column(sql.String)
    hashed_password = sql.Column(sql.String)

    students = sql.orm.relationship("Student", back_populates="owner")
    images = sql.orm.relationship("Image", back_populates="owner")
    faces_students = sql.orm.relationship("FaceStudent", back_populates="owner")
    faces_images = sql.orm.relationship("FaceImage", back_populates="owner")
    reports = sql.orm.relationship("Report", back_populates="owner")

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class Student(database.Base):
    __tablename__ = "students"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey(USERS_ID))
    
    name = sql.Column(sql.String, index=True)
    images = sql.Column(sql.String)
    
    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="students")


class Image(database.Base):
    __tablename__ = "images"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey(USERS_ID))
    
    name = sql.Column(sql.String, index=True)
    image = sql.Column(sql.String)
    
    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="images")


class FaceStudent(database.Base):
    __tablename__ = "faces_students"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey(USERS_ID))
    
    name = sql.Column(sql.String, sql.ForeignKey("students.name"))
    face_locations = sql.Column(sql.JSON)
    face_encodings = sql.Column(sql.JSON)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="faces_students")


class FaceImage(database.Base):
    __tablename__ = "faces_images"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey(USERS_ID))
    
    name = sql.Column(sql.String, sql.ForeignKey("images.name"))
    face_locations = sql.Column(sql.JSON)
    face_encodings = sql.Column(sql.JSON)
    student_names = sql.Column(sql.JSON, default=None)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="faces_images")


class Report(database.Base):
    __tablename__ = "reports"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey(USERS_ID))

    name = sql.Column(sql.String, index=True)
    info = sql.Column(sql.JSON)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="reports")
