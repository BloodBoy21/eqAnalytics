import json
from services.service_base import ServiceBase
from repositories.user_repository import UserRepository

user_service = None


class UserService(ServiceBase):
    def __init__(self, repository):
        self.repository = repository

    @staticmethod
    def get_instance():
        global user_service
        if not user_service:
            user_service = UserService(UserRepository.get_instance())
        return user_service

    def consume(self, data: dict):
        data = json.loads(data)
        print(data)
        type = data.get("type")
        payload = data.get("payload")
        types = {
            "create_user": self.__register,
            "update_coordinates": self.__update_location,
        }
        run = types.get(type, lambda: print(f"Invalid type: {type}"))
        run(payload)

    def __register(self, data):
        self.repository.create(data)
        return data

    def __update_location(self, data):
        self.repository.update_location(data)
        return data
