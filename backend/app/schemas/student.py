from datetime import datetime

from app.schemas.base import StudentBase


class StudentCreate(StudentBase):
    pass


# pylint:disable=duplicate-code
class Student(StudentBase):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True
