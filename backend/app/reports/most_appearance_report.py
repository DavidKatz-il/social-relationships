from typing import Dict, List, Protocol, Union

from app.reports.base import BaseReport


class Data(Protocol):
    student_images: Dict[str, List[str]]


class MostAppearanceReport(BaseReport):

    name = "Most appearance"
    keys = ["Student", "Count"]

    @staticmethod
    def create(data: Data) -> List[Dict[str, Union[str, int]]]:
        total_count = {
            student_name: len(images)
            for student_name, images in data.student_images.items()
        }
        max_count = max(total_count.values())
        report = [
            {
                "Student": student_name,
                "Count": count,
            }
            for student_name, count in total_count.items()
            if count == max_count
        ]
        return report
