from typing import Dict, List, Protocol, Union

from app.reports.base import BaseReport


class Data(Protocol):
    student_images: Dict[str, List[str]]


class TotalAppearReport(BaseReport):

    name = "Total appear"
    keys = ["Student", "Count", "Images"]

    def create(self, data: Data) -> List[Dict[str, Union[str, int]]]:
        report = [
            {
                "Student": student_name,
                "Count": len(image_names),
                "Images": self.join_sorted(image_names),
            }
            for student_name, image_names in data.student_images.items()
        ]
        return report
