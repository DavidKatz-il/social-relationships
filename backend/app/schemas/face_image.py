from datetime import datetime
from typing import List

from app.schemas.base import FaceBase


class FaceImageCreate(FaceBase):
    student_names: List[str]
    face_locations: List[List[int]]
    face_encodings: List[List[float]]


# pylint:disable=duplicate-code
class FaceImage(FaceImageCreate):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True
