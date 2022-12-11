from typing import Dict, List, Protocol, Union

from app.reports.base import BaseReport


class Data(Protocol):
    student_images: Dict[str, List[str]]


class BestiesReport(BaseReport):

    name = "Besties"
    keys = ["Student", "BFF", "Count"]

    @staticmethod
    def create(data: Data) -> List[Dict[str, Union[str, int]]]:
        report = []
        for student_name in data.student_images:
            bff = ""
            count = 0
            for bff_name in data.student_images:
                if student_name == bff_name:
                    continue

                count_intersection = len(
                    set(data.student_images[student_name])
                    & set(data.student_images[bff_name])
                )
                if count_intersection > 0 and count_intersection > count:
                    count = count_intersection
                    bff = bff_name

            if count > 0:
                report.append(
                    {
                        "Student": student_name,
                        "BFF": bff,
                        "Count": count,
                    }
                )

        return report
