from base64 import b64encode
from io import BytesIO

from PIL.Image import Image
from pydantic import BaseModel, ConfigDict

from .bounding_box import BoundingBox


class Prediction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


    bounding_box: BoundingBox
    image: Image

    @property
    def as_json(self) -> dict:
        buffer = BytesIO()
        self.image.save(fp=buffer, format="png")
        return {
            "bounding_box": self.bounding_box.model_dump(),
            "image": b64encode(buffer.getvalue()).decode(),
        }