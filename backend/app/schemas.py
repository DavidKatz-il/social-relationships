from datetime import datetime

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
