from typing import List

from pydantic import BaseModel


class PredictRequest(BaseModel):
    """Incoming request model."""

    feature: str
    data: List[float]
    smoothing_level: float

    class Config:
        """Request example."""

        schema_extra = {
            "example": {
                "feature": "number_of_post_views",
                "data": [142, 138, 171, 164, 143, 73],
                "smoothing_level": 0.5,
            }
        }


class PredictResponse(BaseModel):
    """Response model."""

    feature: str
    predicted_value: float
