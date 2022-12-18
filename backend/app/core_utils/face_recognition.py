from urllib.request import urlopen

import face_recognition
import fastapi


async def get_locations_and_encodings_from_image(image_base64: str):
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
        raise fastapi.HTTPException(
            status_code=400, detail="Cannot recognize a face in the image."
        )

    face_encodings = face_recognition.face_encodings(image, face_locations)

    locations = list(map(list, face_locations))
    encodings = list(map(lambda e: e.tolist(), face_encodings))

    return locations, encodings


async def get_locations_and_encodings_from_images(images: list):
    locations, encodings = [], []
    for image_base64 in images:
        face_locations, face_encodings = await get_locations_and_encodings_from_image(
            image_base64
        )
        if len(face_locations) != 1:
            raise fastapi.HTTPException(
                status_code=400, detail="Must be only on face in the image."
            )
        locations.append(face_locations[0])
        encodings.append(face_encodings[0])

    return locations, encodings
