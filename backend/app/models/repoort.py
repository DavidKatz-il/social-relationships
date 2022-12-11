from datetime import datetime

import sqlalchemy as sql

from app import database


class Report(database.Base):
    __tablename__ = "reports"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))

    name = sql.Column(sql.String, index=True)
    info = sql.Column(sql.JSON)

    datetime_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    datetime_updated = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = sql.orm.relationship("User", back_populates="reports")
