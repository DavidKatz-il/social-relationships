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

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class Person(database.Base):
    __tablename__ = "persons"
    __table_args__ = (sql.UniqueConstraint("name", "owner_id"),)

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    name = sql.Column(sql.String, index=True)
    images = sql.Column(sql.String, default="")
    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="persons")
