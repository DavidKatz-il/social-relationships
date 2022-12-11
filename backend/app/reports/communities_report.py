from typing import Callable, Dict, Iterable, List, Optional, Protocol, Union

from networkx import Graph
from networkx.algorithms.community import louvain_communities

from app.reports.base import BaseGraphReport


class Data(Protocol):
    image_students: Dict[str, List[str]]


class CommunitiesReport(BaseGraphReport):

    name = "Communities"
    keys = ["Community", "Members"]

    def create(
        self,
        data: Data,
    ) -> List[Dict[str, Union[str, int]]]:
        graph = self.create_graph(data.image_students.values())
        communities = map(sorted, louvain_communities(graph))
        report = [
            {
                "Community": str(i),
                "Members": self.join_sorted(community),
            }
            for i, community in enumerate(communities)
        ]
        return report
