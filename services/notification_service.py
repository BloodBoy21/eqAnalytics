from services.Emitter import KafkaProducer
from services.service_base import ServiceBase
import queue
import json

notification_producer = KafkaProducer("notification")
notification_service = None


class Notification:
    def __init__(self, user_id: int, payload: dict, type: str):
        self.user_id = user_id
        self.payload = payload
        self.type = type

    def get_notification(self):
        return {"user_id": self.user_id, "payload": self.payload, "type": self.type}

    def to_json(self):
        return json.dumps(self.get_notification())


class NotificationService(ServiceBase):
    def __init__(self, repository):
        self.repository = repository
        self.queue = queue.Queue()

    @staticmethod
    def get_instance():
        global notification_service
        if not notification_service:
            notification_service = NotificationService()
        return notification_service

    def send(self, data):
        self.addToQueue(data)
        self.__emit()

    def __emit(self):
        data = self.queue.get()
        if not data:
            return
        notification_producer.produce(data)
        self.__emit()
