import base64
import io
from abc import ABC
from typing import List, Optional

import matplotlib.pyplot as plt

from app.core_utils.const import Const
from app.core_utils.image import draw_face_boxes
from app.reports.base.base_report import BaseReport


class BaseImageReport(BaseReport, ABC):
    def plt_to_base_64(self, image_format: Optional[str] = "png") -> str:
        bytes_buffer = io.BytesIO()
        plt.savefig(bytes_buffer, format=image_format, bbox_inches="tight")
        base_64 = self.image_base_64(bytes_buffer, image_format)
        plt.close()
        return base_64

    @staticmethod
    def image_base_64(bytes_buffer, image_format):
        base_64 = (
            base64.b64encode(bytes_buffer.getvalue()).decode("utf-8").replace("\n", "")
        )
        return f"{Const.image.BASE64_PREFIX.value.format(image_format)}{base_64}"

    @staticmethod
    def get_image_draw_boxes(
        image: str, names: List[str], locations: List[List[int]]
    ) -> str:
        return draw_face_boxes(image, names, locations)
