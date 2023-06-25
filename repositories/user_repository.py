from models.user_model import User
from shared.db import get_db
from math import radians, degrees, sin, cos, asin

user_repository = None


class UserRepository:
    def __init__(self) -> None:
        self.session = get_db()

    @staticmethod
    def get_instance():
        global user_repository
        if not user_repository:
            user_repository = UserRepository()
        return user_repository

    def create(self, data: dict):
        user = User(**data)
        return self.save(user)

    def update_location(self, data: dict):
        user = self.get_user_by_id(data.get("user_id"))
        user.lat = data.get("lat")
        user.lon = data.get("lon")
        return self.save(user)

    def save(self, row):
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def get_user_by_id(self, user_id) -> User:
        return self.session.query(User).filter_by(user_id=user_id).first()

    def get_users_in_radius(self, longitude, latitude, radius):
        # Calculate the bounding box of the search area
        bbox = self.calculate_bounding_box(latitude, longitude, radius)
        # Query the database for users within the bounding box
        users = (
            self.session.query(User)
            .filter(
                User.lon.between(bbox["min_lon"], bbox["max_lon"]),
                User.lat.between(bbox["min_lat"], bbox["max_lat"]),
            )
            .all()
        )

        return users

    def calculate_bounding_box(self, center_lat, center_lon, radius_km):
        # Convert center latitude, longitude, and radius to radians
        center_lat_rad = radians(center_lat)
        center_lon_rad = radians(center_lon)
        radius_rad = radius_km / 6371.0  # Approximate radius of the Earth (in km)

        # Calculate minimum and maximum latitude
        min_lat = degrees(center_lat_rad - radius_rad)
        max_lat = degrees(center_lat_rad + radius_rad)

        # Calculate minimum and maximum longitude
        delta_lon = asin(sin(radius_rad) / cos(center_lat_rad))
        min_lon = degrees(center_lon_rad - delta_lon)
        max_lon = degrees(center_lon_rad + delta_lon)

        return {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon,
        }
