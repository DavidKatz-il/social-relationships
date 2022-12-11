from dataclasses import dataclass
from enum import Enum


class FaceConst(Enum):
    UNKNOWN: str = "Unknown"


class UserConst(Enum):
    JWT_SECRET: str = "special-jwt-secret"
    TOKEN_TYPE: str = "bearer"


class ImageConst(Enum):
    BASE64_PREFIX: str = "data:image/{};base64,"


@dataclass
class Const:

    face = FaceConst
    user = UserConst
    image = ImageConst
