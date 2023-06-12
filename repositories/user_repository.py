from models.user_model import User
import math

user_repository = None


class EarthquakeRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_instance():
        global user_repository
        if not user_repository:
            user_repository = EarthquakeRepository()
        return user_repository

    def get_user_by_id(self, user_id):
        return User.query.filter_by(user_id=user_id).first()

    def get_users_in_radius(self, longitude, latitude, radius):
        # Calculate the bounding box of the search area
        bbox = self.get_bounding_box(longitude, latitude, radius)

        # Query the database for users within the bounding box
        users = User.query.filter(
            User.lon.between(bbox["min_lon"], bbox["max_lon"]),
            User.lat.between(bbox["min_lat"], bbox["max_lat"]),
        ).all()

        # Filter the users by distance from the center point
        users = [
            user
            for user in users
            if self.distance(user.lon, user.lat, longitude, latitude) <= radius
        ]

        return users

    def get_bounding_box(self, longitude, latitude, radius):
        # Calculate the bounding box of the search area
        earth_radius = 6371  # km
        lat_range = radius / earth_radius * (180 / math.pi)
        lon_range = lat_range / math.cos(latitude * (math.pi / 180))
        min_lat = latitude - lat_range
        max_lat = latitude + lat_range
        min_lon = longitude - lon_range
        max_lon = longitude + lon_range
        return {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon,
        }

    def distance(self, lon1, lat1, lon2, lat2):
        # Calculate the distance between two points on the Earth's surface
        earth_radius = 6371  # km
        dlon = math.radians(lon2 - lon1)
        dlat = math.radians(lat2 - lat1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
        return distance
