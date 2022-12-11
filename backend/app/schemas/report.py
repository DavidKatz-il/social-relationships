from typing import Dict, List, Union

from app.schemas.base import ReportBase


class ReportCreate(ReportBase):
    info: Dict[Union[int, str], List]


class Report(ReportCreate):
    id: int

    class Config:
        orm_mode = True


class ReportInfo(ReportBase):
    id: int

    class Config:
        orm_mode = True
