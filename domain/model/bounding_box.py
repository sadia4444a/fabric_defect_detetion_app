from pydantic import BaseModel


class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    class_id: int
    confidence: float
    label: str

    @property
    def center(self) -> tuple[int, int]:
        return int(self.x + self.width // 2), int(self.y + self.height // 2)

    @property
    def crop_rect(self) -> tuple:
        return self.x, self.y, self.x + self.width, self.y + self.height

    def copy(
        self,
        x1: int | None = None,
        y1: int | None = None,
        x2: int | None = None,
        y2: int | None = None,
        class_id: int | None = None,
        confidence: float | None = None,
    ) -> "BoundingBox":
        return BoundingBox(
            x1=x1 if x1 else self.x1,
            y1=y1 if y1 else self.y1,
            x2=x2 if x2 else self.x2,
            y2=y2 if y2 else self.y2,
            class_id=class_id if class_id else self.class_id,
            confidence=confidence if confidence else self.confidence,
        )