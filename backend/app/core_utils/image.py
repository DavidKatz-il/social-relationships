import base64
import io
import re
from typing import List

from PIL import Image, ImageDraw, ImageFont

from app import FONT_PATH
from app.core_utils.const import Const


def base64_to_image(image: str) -> Image:
    base64_prefix = Const.image.BASE64_PREFIX.value.format(".+")
    image_data = re.sub(rf"^{base64_prefix}", "", image)
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    return image


def image_to_base64(image: Image, image_format: str, encoding: str) -> str:
    base64_prefix = Const.image.BASE64_PREFIX.value.format(format)
    bytes_buffer = io.BytesIO()
    image.save(bytes_buffer, format=image_format)
    image_base_64 = (
        base64.b64encode(bytes_buffer.getvalue()).decode(encoding).replace("\n", "")
    )
    image.close()
    return f"{base64_prefix}{image_base_64}"


# pylint:disable=too-many-locals
def draw_face_boxes(
    image: str,
    names: List[str],
    locations: List[List[int]],
    encoding: str = "utf-8",
    image_format: str = "png",
) -> str:
    image = base64_to_image(image)
    draw = ImageDraw.Draw(image)

    for (top, right, bottom, left), student_name in zip(locations, names):
        student_name = student_name.encode(encoding)
        text_width, text_height = draw.textsize(student_name)
        text_width, text_height = text_width * 5, text_height * 5

        color = (0, 0, 255)  # blue
        if student_name == bytes(Const.face.UNKNOWN.value, encoding):
            color = (255, 0, 0)  # red

        # draw the box around the face
        draw.rectangle(((left, top), (right, bottom)), outline=color)
        draw.rectangle(
            ((left, bottom), (right, bottom + int(image.size[0] * 0.02))),
            fill=color,
            outline=color,
        )

        # draw the name of the person
        font = ImageFont.truetype(FONT_PATH, int(image.size[0] * 0.015))
        draw.text(
            (left, bottom),
            student_name.decode(encoding),
            fill=(255, 255, 255, 255),
            font=font,
        )

    image_base_64 = image_to_base64(image, image_format, encoding)
    return image_base_64
