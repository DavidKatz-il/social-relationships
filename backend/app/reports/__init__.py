from typing import Dict, Iterator, List, Optional, Protocol, Type, Union

from app.reports.basties_report import BestiesReport
from app.reports.communities_report import CommunitiesReport
from app.reports.friends_report import FriendsReport
from app.reports.graph_report import GraphReport
from app.reports.image_students import ImageStudentsReport
from app.reports.images_face_recognition_report import ImagesFaceRecognitionReport
from app.reports.images_with_unknowns_report import ImagesWithUnknownsReport
from app.reports.most_appearance_report import MostAppearanceReport
from app.reports.not_appear_report import NotAppearReport
from app.reports.total_appear_report import TotalAppearReport


class Data(Protocol):
    student_images: Optional[Dict[str, List[str]]]
    image_students: Optional[Dict[str, List[str]]]
    all_student_names: Optional[List[str]]
    images: Optional[List[Dict[str, Union[List[str], List[List[int]]]]]]


class InterfaceReport(Protocol):
    name: str
    keys: List[str]

    def create(self, data: Data, *args, **kwargs) -> List[Dict[str, Union[str, int]]]:
        """
        Each report must have a method that is called `create` that will return the created report.
        """


class ReportFactory:
    def __init__(self):
        self._creators: Dict[str, InterfaceReport] = {}

    def register_report_creator(self, report_creator: InterfaceReport) -> None:
        self._creators[report_creator.name] = report_creator

    def register_report_creators(self, report_creators: List[InterfaceReport]) -> None:
        for report_creator in report_creators:
            self.register_report_creator(report_creator)

    def get_report_creator(self, name: str, **kwargs) -> InterfaceReport:
        creator = self._creators.get(name)
        if not creator:
            raise ValueError(name)
        return creator(**kwargs)

    def creators(self) -> Iterator[Type[InterfaceReport]]:
        for report_creator in self._creators.values():
            yield report_creator


report_factory = ReportFactory()
report_factory.register_report_creators(
    [
        BestiesReport,
        CommunitiesReport,
        FriendsReport,
        GraphReport,
        ImageStudentsReport,
        ImagesFaceRecognitionReport,
        ImagesWithUnknownsReport,
        MostAppearanceReport,
        NotAppearReport,
        TotalAppearReport,
    ]
)
