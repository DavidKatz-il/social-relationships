from typing import Optional

from app.schemas.base import Base, UserBase


class UserCreate(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserUpdate(Base):
    email: Optional[str]
    teacher_name: Optional[str]
    school_name: Optional[str]
    hashed_password: Optional[str]


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInfo(Base):
    students_count: int
    images_count: int
