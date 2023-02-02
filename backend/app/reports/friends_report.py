from typing import Dict, List, Protocol, Union

from app.reports.base import BaseReport


class Data(Protocol):
    student_images: Dict[str, List[str]]


class FriendsReport(BaseReport):
    name = "Friends"
    keys = ["Student", "Count", "Students"]

    def create(self, data: Data) -> List[Dict[str, Union[str, int]]]:
        student_friends = {}
        for student_name, student_image_names in data.student_images.items():
            for friend_name, friend_image_names in data.student_images.items():
                if student_name == friend_name:
                    continue
                if set(student_image_names) & set(friend_image_names):
                    student_friends[student_name] = student_friends.get(
                        student_name, []
                    )
                    student_friends[student_name].append(friend_name)

        report = [
            {
                "Student": studend_name,
                "Count": len(friends),
                "Students": self.join_sorted(friends),
            }
            for studend_name, friends in student_friends.items()
        ]
        return report
