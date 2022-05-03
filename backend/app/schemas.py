from datetime import datetime
from typing import List

from pydantic import BaseModel


class _UserBase(BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class _PersonBase(BaseModel):
    name: str
    images: str


class PersonCreate(_PersonBase):
    pass


class Person(_PersonBase):
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
    # class Config:
    #     arbitrary_types_allowed = True


class FacePersonCreate(_FaceBase):
    face_locations: List[List[int]]
    face_encodings: List[List[float]]


class FacePerson(FacePersonCreate):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True

class FaceImageCreate(_FaceBase):
    person_names: List[str]
    face_locations: List[List[int]]
    face_encodings: List[List[float]]


class FaceImage(FaceImageCreate):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True
