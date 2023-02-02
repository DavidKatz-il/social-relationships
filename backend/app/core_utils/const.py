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


class APIMessagesConst(str, Enum):
    ROOT = "Social Relationships API"
    UPDATED = "Successfully Updated."
    DELETED = "Successfully Deleted."
    CREATE_MATCH_FACES = "Successfully finished matcheing all faces."


class ExceptionMessagesConst(str, Enum):
    USER_NOT_EXIST = "Invalid Credentials."
    EMAIL_EXIST = "Email already in use."
    EMAIL_INVALID = "Invalid email address."
    STUDENT_IMAGE_ONE_FACE = "Must be only one face in a student image"
    STUDENT_EXIST = "Email already in use."
    STUDENT_REQUIREMENTS = "Student must have a name and at least one image."
    IMAGE_WITHOUT_FACES = "Cannot recognize a face in the image."
    PASSWORD_REQUIREMENTS = (
        "The password must contain at least {min_pass_len} characters."
    )
    IMAGE_EXIST = "Image already exist."
    IMAGE_REQUIREMENTS = "Image must have a name and a image."


@dataclass
class Const:
    face = FaceConst
    user = UserConst
    image = ImageConst
    app = APPConst
    api_messages = APIMessagesConst
    exception_messages = ExceptionMessagesConst
