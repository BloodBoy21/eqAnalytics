import queue
from repositories.earthquake_repository import EarthquakeRepository
from services.service_base import ServiceBase
import json
from lib.Earthquake import Earthquake
from repositories.user_repository import UserRepository

earthquake_service = None


class EarthquakeService(ServiceBase):
    def __init__(self, repository):
        self.repository = repository
        self.queue = queue.Queue()
        self.user_repository = UserRepository.get_instance()

    @staticmethod
    def get_instance():
        global earthquake_service
        if not earthquake_service:
            earthquake_service = EarthquakeService(EarthquakeRepository.get_instance())
        return earthquake_service

    def consume(self, data):
        data = json.loads(data)
        data = Earthquake(**data)
        self.addToQueue(data)

    def addToQueue(self, data):
        self.queue.put(data)
        self.repository.save(data)
        self.get_user_in_area()

    def get_user_in_area(self):
        data = self.queue.get()
        data = self.user_repository.get_users_in_radius(
            data.coordinates.lon, data.coordinates.lat, 10
        )
        print(data)
