from pydantic import BaseModel
from typing import Optional


# -------------------------
# Prediction API Schemas
# -------------------------

class AccidentInput(BaseModel):
    latitude: float
    longitude: float
    speed_limit: float
    hour: int
    month: int
    day_of_week: int
    number_of_deaths: int
    number_of_injuries: int


class PredictionOutput(BaseModel):
    severity_class: int
    confidence: float
    model_used: str
