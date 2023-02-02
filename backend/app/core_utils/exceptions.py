class ImageFaceError(Exception):
    """Exception raised for errors in the number of faces in an image.

    Attributes:
        num_of_faces: the num of faces that exist in the image
        message -- explanation of the error
    """

    def __init__(
        self, num_of_faces: int, message="Image with only one face is expected."
    ):
        self.num_of_faces = num_of_faces
        self.message = message
        super().__init__(self.message)
