import sqlalchemy as sql
from passlib.hash import bcrypt

from app import database


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
