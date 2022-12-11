from abc import ABC
from typing import List


class BaseReport(ABC):
    @staticmethod
    def join_sorted(items: List[str]) -> str:
        return ", ".join(sorted(items))
