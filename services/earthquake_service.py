import queue
from repositories.earthquake_repository import EarthquakeRepository
from services.service_base import ServiceBase
from services.notification_service import NotificationService, Notification
import json
from lib.Earthquake import Earthquake
from repositories.user_repository import UserRepository

earthquake_service = None
notification_service = NotificationService.get_instance()


class EarthquakeService(ServiceBase):
    def __init__(self, repository):
        self.repository = repository
        self.queue = queue.Queue()
        self.user_repository = UserRepository.get_instance()
        self.notification_queue = queue.Queue()

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
        self.get_user_in_area()
        for event in self.get_events():
            users = event.get("users", [])
            payload = {
                "earthquake_id": event.get("_id"),
                "message": "There is an earthquake in your area please be careful",
                "coordinates": vars(event.get("coordinates", {})),
                "magnitude": event.get("magnitude"),
                "place": event.get("place"),
            }
            for user in users:
                notification = Notification(user.user_id, payload, "earthquake")
                notification_service.send(notification.to_json())

    def addToQueue(self, data):
        self.queue.put(data)
        self.repository.save(data)

    def get_user_in_area(self):
        try:
            data = self.queue.get(block=False)
        except queue.Empty:
            return
        users = self.user_repository.get_users_in_radius(
            data.coordinates.lon, data.coordinates.lat, 10
        )
        payload = {
            **vars(data),
            "users": users,
        }
        self.notification_queue.put(payload)
        return self.get_user_in_area()

    def get_events(self):
        try:
            yield self.notification_queue.get(block=False)
        except queue.Empty:
            pass
