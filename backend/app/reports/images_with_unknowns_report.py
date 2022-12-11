from typing import Dict, List, Protocol, Union

from app.core_utils.const import FaceConst
from app.reports.base import BaseReport


class Data(Protocol):
    image_students: Dict[str, List[str]]


class ImagesWithUnknownsReport(BaseReport):

    name = "Images with unknowns"
    keys = ["Image", "Count"]

    @staticmethod
    def create(data: Data) -> List[Dict[str, Union[str, int]]]:
        report = [
            {
                "Image": image_name,
                "Count": students.count(FaceConst.UNKNOWN.value),
            }
            for image_name, students in data.image_students.items()
            if FaceConst.UNKNOWN.value in students
        ]
        return report
