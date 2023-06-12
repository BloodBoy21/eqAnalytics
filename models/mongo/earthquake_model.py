from pydantic import BaseModel, Field
from shared.mongo import database
from datetime import datetime


class Coordinates(BaseModel):
    type: str = ""
    lon: float = 0.0
    lat: float = 0.0
    elevation: float = 0.0


class Earthquake(BaseModel):
    magnitude: float = Field(...)
    place: str = ""
    time: int = 0
    id: str = Field(...)
    coordinates: Coordinates = Coordinates()


collection = database.get_collection("earthquakes")
