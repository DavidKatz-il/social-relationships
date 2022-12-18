from typing import Dict, List, Protocol, Union

from app.reports.base import BaseImageReport


class Data(Protocol):
    images: List[Dict[str, Union[List[str], List[List[int]]]]]


class ImagesFaceRecognitionReport(BaseImageReport):

    name = "Images"
    keys = ["Image"]

    def create(self, data: Data) -> List[Dict[str, Union[str, int]]]:
        report = [
            {
                "Image": self.get_image_draw_boxes(
                    image["image"],
                    image["student_names"],
                    image["face_locations"],
                )
            }
            for image in data.images
        ]
        return report
