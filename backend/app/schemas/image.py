from datetime import datetime

from app.schemas.base import ImageBase


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    owner_id: int
    datetime_created: datetime
    datetime_updated: datetime

    class Config:
        orm_mode = True
