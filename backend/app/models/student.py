from datetime import datetime

import sqlalchemy as sql

from app import database


class Student(database.Base):
    __tablename__ = "students"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))

    name = sql.Column(sql.String, index=True)
    images = sql.Column(sql.String)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="students")
