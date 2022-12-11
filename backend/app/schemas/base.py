from pydantic import BaseModel


class Base(BaseModel):
    """Our BaseModel"""


class FaceBase(Base):
    name: str


class ReportBase(Base):
    name: str


class ImageBase(Base):
    name: str
    image: str


class StudentBase(BaseModel):
    name: str
    images: str


class UserBase(Base):
    email: str
    teacher_name: str
    school_name: str
