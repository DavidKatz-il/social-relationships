from datetime import datetime
from typing import Dict, List, Optional, Union
from typing_extensions import Self

from pydantic import BaseModel


class _UserBase(BaseModel):
    email: str
    teacher_name: str
    school_name: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[str]
    teacher_name: Optional[str]
    school_name: Optional[str]
    hashed_password: Optional[str]


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    students_count: int
    images_count: int


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
    name: str


class ReportCreate(_ReportBase):
    info: Dict[Union[int, str], List]


class Report(ReportCreate):
    id: int

    class Config:
        orm_mode = True


class ReportInfo(_ReportBase):
    id: int

    class Config:
        orm_mode = True
