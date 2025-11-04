from pydantic import BaseModel


class PredictionPayload(BaseModel):
    image: str  
    