from datetime import datetime

import sqlalchemy as sql

from app import database


class FaceStudent(database.Base):
    __tablename__ = "faces_students"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))

    name = sql.Column(sql.String, sql.ForeignKey("students.name"))
    face_locations = sql.Column(sql.JSON)
    face_encodings = sql.Column(sql.JSON)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="faces_students")
