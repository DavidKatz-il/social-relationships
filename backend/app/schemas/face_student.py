from datetime import datetime
from typing import List

from app.schemas.base import FaceBase


class FaceStudentCreate(FaceBase):
    face_locations: List[List[int]]
    face_encodings: List[List[float]]


class FaceStudent(FaceStudentCreate):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True
