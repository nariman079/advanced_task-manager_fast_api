from pydantic import BaseModel

class LocationSchema(BaseModel):
    name: str
    longitude: float
    latitude: float

class TaskSchemaBase(BaseModel):
    name: str
    location: LocationSchema | None = None
