from typing import Annotated

import redis
from fastapi import FastAPI, Depends, Body

from database import get_redis_connection
from schemas import LocationSchema, PlaceAroundLocationSearchSchema
from services import LocationDB

app = FastAPI()

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/locations/", response_model=LocationSchema)
async def add_location(
        location: Annotated[LocationSchema, Body()],
        db: redis.Redis = Depends(get_redis_connection)
):
    location_db = LocationDB(db)
    return await location_db.add_location(location)

@app.get("/locations/distance/", response_model=float)
async def get_distance(place_one: str, place_two: str, unit: str = 'km', db: redis.Redis = Depends(get_redis_connection)):
    location_db = LocationDB(db)
    return await location_db.get_distance(place_one, place_two, unit)

@app.post("/locations/around/", response_model=list[LocationSchema])
async def find_places_around_location(place_around_data: PlaceAroundLocationSearchSchema, db: redis.Redis = Depends(get_redis_connection)):
    location_db = LocationDB(db)
    return await location_db.find_places_around_location(place_around_data)