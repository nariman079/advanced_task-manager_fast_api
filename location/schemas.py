from pydantic import BaseModel

class LocationSchema(BaseModel):
    name: str
    longitude: float
    latitude: float


class PlaceAroundLocationSearchSchema(BaseModel):
    place: str
    radius: float
    unit: str

