from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class _UserBase(BaseModel):
    email: str
    teacher_name: str
    school_name: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class _StudentBase(BaseModel):
    name: str
    images: str


class StudentCreate(_StudentBase):
    pass


class Student(_StudentBase):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True


class _ImageBase(BaseModel):
    name: str
    image: str


class ImageCreate(_ImageBase):
    pass


class Image(_ImageBase):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True


class _FaceBase(BaseModel):
    name: str


class FaceStudentCreate(_FaceBase):
    face_locations: List[List[int]]
    face_encodings: List[List[float]]


class FaceStudent(FaceStudentCreate):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True


class FaceImageCreate(_FaceBase):
    student_names: List[str]
    face_locations: List[List[int]]
    face_encodings: List[List[float]]


class FaceImage(FaceImageCreate):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True


class _ReportBase(BaseModel):
    id: int
    name: str


class ReportCreate(_ReportBase):
    pass


class Report(ReportCreate):
    info: Dict[int, List]

    class Config:
        orm_mode = True

class ReportInfo(ReportCreate):
    class Config:
        orm_mode = True
