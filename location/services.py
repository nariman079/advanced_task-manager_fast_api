import logging
import redis

from schemas import (LocationSchema,
                              PlaceAroundLocationSearchSchema)


class LocationDB:
    """Работа с локациями в БД"""
    def __init__(self, db: redis.Redis):
        self.db = db

    async def add_location(
        self,
        location: LocationSchema
    ) -> LocationSchema:
        """
        Добавить локацию в БД.
        """
        self.db.geoadd('locations',
                             (
                                 location.longitude,
                                 location.latitude,
                                 location.name
                             )
                             )
        logging.info(
            msg=f"Местоположение {location.name} добавлено с координатами "
                f"({location.longitude}, {location.latitude}) ",
        )
        return location

    async def get_distance(
        self,
        place_one: str,
        place_two: str,
        unit: str = 'km'
    ) -> float:
        """
        Получить расстояние между двумя местоположениями.
        """
        distance = self.db.geodist('locations', place_one, place_two, unit)
        if distance:
            print(f"Расстояние между {place_one} и {place_two}: {distance} {unit}")
        else:
            print("Не удалось найти одно или оба местоположения.")
        return distance

    async def find_places_around_location(
        self,
        place_around_data: PlaceAroundLocationSearchSchema
    ) -> list[LocationSchema]:
        """
        Найти локацию в радиусе от другой локации.
        """
        places = self.db.georadiusbymember(
        'locations',
            place_around_data.place,
            place_around_data.radius,
            place_around_data.unit
        )
        if places:
            logging.info(msg=f"Места в радиусе {place_around_data.radius}"
                             f" {place_around_data.unit} от "
                             f"{place_around_data.place}: {places}"
                         )
        else:
            logging.error(msg=f"Никаких мест не найдено в радиусе "
                              f"{place_around_data.radius} "
                              f"{place_around_data.unit} от "
                              f"{place_around_data.place}.")

        return [LocationSchema(**location) for location in places]

