from datetime import datetime

import sqlalchemy as sql

from app import database


class FaceImage(database.Base):
    __tablename__ = "faces_images"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))

    name = sql.Column(sql.String, sql.ForeignKey("images.name"))
    face_locations = sql.Column(sql.JSON)
    face_encodings = sql.Column(sql.JSON)
    student_names = sql.Column(sql.JSON, default=None)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="faces_images")
