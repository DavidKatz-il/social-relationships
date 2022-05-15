from datetime import datetime

import sqlalchemy as sql
from passlib.hash import bcrypt

from app import database


class User(database.Base):
    __tablename__ = "users"
    
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    hashed_password = sql.Column(sql.String)

    persons = sql.orm.relationship("Person", back_populates="owner")
    images = sql.orm.relationship("Image", back_populates="owner")
    faces_persons = person_faces = sql.orm.relationship("FacePerson", back_populates="owner")
    faces_images = sql.orm.relationship("FaceImage", back_populates="owner")

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class Person(database.Base):
    __tablename__ = "persons"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    
    name = sql.Column(sql.String, index=True)
    images = sql.Column(sql.String)
    
    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="persons")


class Image(database.Base):
    __tablename__ = "images"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    
    name = sql.Column(sql.String, index=True)
    image = sql.Column(sql.String)
    
    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="images")


class FacePerson(database.Base):
    __tablename__ = "faces_persons"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    
    name = sql.Column(sql.String, sql.ForeignKey("persons.name"))
    face_locations = sql.Column(sql.JSON)
    face_encodings = sql.Column(sql.JSON)
    
    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="faces_persons")


class FaceImage(database.Base):
    __tablename__ = "faces_images"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))

    name = sql.Column(sql.String, sql.ForeignKey("images.name"))
    face_locations = sql.Column(sql.JSON)
    face_encodings = sql.Column(sql.JSON)
    person_names = sql.Column(sql.JSON, default=None)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="faces_images")


class Reports(database.Base):
    __tablename__ = "reports"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))

    name = sql.Column(sql.String, index=True)
    info = sql.Column(sql.String)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="reports")
