from typing import List, Tuple, Union
from urllib.request import urlopen

import face_recognition

from app.core_utils.exceptions import ImageFaceError


async def get_locations_and_encodings_from_image(
    image_base64: str,
) -> Tuple[Union[list, List[List[int]]], Union[list, List[List[float]]]]:
    def get_locations(image):
        locations = face_recognition.face_locations(
            image, number_of_times_to_upsample=1, model="hog"
        )
        if len(locations) == 0:
            locations = face_recognition.face_locations(
                image, number_of_times_to_upsample=2, model="cnn"
            )
        return locations

    with urlopen(image_base64) as image:
        image = face_recognition.load_image_file(image)

    face_locations = get_locations(image)
    if len(face_locations) == 0:
        return [], []

    face_encodings = face_recognition.face_encodings(image, face_locations)

    locations = list(map(list, face_locations))
    encodings = list(map(lambda e: e.tolist(), face_encodings))

    return locations, encodings


async def get_locations_and_encodings_from_images_with_only_one_face(
    images: List[str],
) -> Tuple[Union[list, List[List[int]]], Union[list, List[List[float]]]]:
    locations, encodings = [], []
    for image_base64 in images:
        face_locations, face_encodings = await get_locations_and_encodings_from_image(
            image_base64
        )
        num_of_faces_in_image = len(face_locations)
        if num_of_faces_in_image != 1:
            raise ImageFaceError(num_of_faces_in_image)
        locations.append(face_locations[0])
        encodings.append(face_encodings[0])

    return locations, encodings
