import queue
from repositories.earthquake_repository import EarthquakeRepository
from services.service_base import ServiceBase
import json
from lib.Earthquake import Earthquake

earthquake_service = None


class EarthquakeService(ServiceBase):
    def __init__(self, repository):
        self.repository = repository
        self.queue = queue.Queue()

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
