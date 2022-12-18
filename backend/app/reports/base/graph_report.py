import base64
import io
import itertools
from abc import ABC
from typing import List, Optional

import matplotlib.pyplot as plt
import networkx as nx

from app.reports.base.base_report import BaseReport


class BaseGraphReport(BaseReport, ABC):
    @staticmethod
    def create_graph(lists_students: List[List[str]]) -> nx.Graph:
        edge_list = [
            tuple(pair)
            for studens in lists_students
            for pair in itertools.combinations(studens, 2)
        ]
        graph = nx.from_edgelist(edge_list)
        return graph

    @staticmethod
    def get_graph_draw_as_base64(graph: nx.Graph, font_size: Optional[int] = 8) -> str:
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos=pos, with_labels=True, node_color="skyblue", font_size=8)
        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=nx.get_edge_attributes(graph, "weight"),
            rotate=False,
            font_size=font_size,
        )
        bytes_buffer = io.BytesIO()
        plt.savefig(bytes_buffer, format="png", bbox_inches="tight")
        img_base64 = (
            base64.b64encode(bytes_buffer.getvalue()).decode("utf-8").replace("\n", "")
        )
        plt.close()
        return img_base64
