from models.mongo.earthquake_model import Earthquake, collection

earthquake_repository = None


class EarthquakeRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_instance():
        global earthquake_repository
        if not earthquake_repository:
            earthquake_repository = EarthquakeRepository()
        return earthquake_repository

    def save(self, data):
        data_parsed = self.__format_to_save(data)
        data = Earthquake(**data_parsed)
        collection.insert_one(data.dict())
        return data

    def __format_to_save(self, data):
        return {
            "magnitude": data.magnitude,
            "place": data.place if data.place else "",
            "time": data.time,
            "id": data.get_id(),
            "coordinates": {
                "type": data.coordinates.type,
                "lon": data.coordinates.lon,
                "lat": data.coordinates.lat,
                "elevation": data.coordinates.elevation,
            },
        }
