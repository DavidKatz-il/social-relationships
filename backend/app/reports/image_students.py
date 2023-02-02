from typing import Dict, List, Protocol, Union

from app.reports.base import BaseReport


class Data(Protocol):
    image_students: Dict[str, List[str]]


class ImageStudentsReport(BaseReport):
    name = "Who is in the image"
    keys = ["Image", "Count", "Students"]

    def create(self, data: Data) -> List[Dict[str, Union[str, int]]]:
        report = [
            {
                "Image": image_name,
                "Count": len(students),
                "Students": self.join_sorted(students),
            }
            for image_name, students in data.image_students.items()
        ]
        return report
