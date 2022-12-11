from typing import Dict, List, Protocol, Union

from app.reports.base import BaseImageGraphReport


class Data(Protocol):
    image_students: Dict[str, List[str]]
    all_student_names: List[str]


class GraphReport(BaseImageGraphReport):

    name = "Graph"
    keys = ["Image"]

    def create(self, data: Data) -> List[Dict[str, Union[str, int]]]:
        graph = self.create_graph(data.image_students.values())
        report = [{"Image": self.plt_to_base_64()}]

        if sorted(graph.nodes) != sorted(data.all_student_names):
            graph.add_nodes_from(data.all_student_names)
            report.append({"Image": self.get_image_draw_graph(graph)})

        return report
