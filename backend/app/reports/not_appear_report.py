from typing import Dict, List, Protocol, Union

from app.reports.base import BaseReport


class Data(Protocol):
    student_images: Dict[str, List[str]]
    all_student_names: List[str]


class NotAppearReport(BaseReport):

    name = "Not appear"
    keys = ["Student"]

    @staticmethod
    def create(data: Data) -> List[Dict[str, Union[str, int]]]:
        missing_students = set(data.all_student_names) - set(data.student_images)
        report = [
            {
                "Student": studend_name,
            }
            for studend_name in missing_students
        ]
        return report
