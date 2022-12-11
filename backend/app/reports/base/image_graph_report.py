from abc import ABC
from typing import Optional

import networkx as nx

from app.reports.base.graph_report import BaseGraphReport
from app.reports.base.image_report import BaseImageReport


class BaseImageGraphReport(BaseImageReport, BaseGraphReport, ABC):
    @staticmethod
    def draw_graph(graph: nx.Graph, font_size: Optional[int] = 8):
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos=pos, with_labels=True, node_color="skyblue", font_size=8)
        edge_labels = nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=nx.get_edge_attributes(graph, "weight"),
            rotate=False,
            font_size=font_size,
        )
        return edge_labels

    def get_image_draw_graph(self, graph: nx.Graph) -> str:
        self.draw_graph(graph)
        return self.plt_to_base_64()
