from dataclasses import dataclass
from enum import Enum


class FaceConst(Enum):
    UNKNOWN: str = "Unknown"


class UserConst(Enum):
    JWT_SECRET: str = "special-jwt-secret"
    TOKEN_TYPE: str = "bearer"


class ImageConst(Enum):
    BASE64_PREFIX: str = "data:image/{};base64,"


class APPConst(Enum):
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    TITLE: str = "Social Relationships - API"


class APIMessagesConst(Enum):
    ROOT: str = "Social Relationships API"
    UPDATED: str = "Successfully Updated."
    DELETED: str = "Successfully Deleted."
    CREATE_MATCH_FACES: str = "Successfully finished matcheing all faces."
    USER_NOT_EXIST: str = "Invalid Credentials."
    EMAIL_ALREADY_EXIST: str = "Email already in use."


@dataclass
class Const:

    face = FaceConst
    user = UserConst
    image = ImageConst
    app = APPConst
    api_messages = APIMessagesConst
