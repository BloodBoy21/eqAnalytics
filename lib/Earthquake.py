class Earthquake:
    def __init__(self, **kwargs):
        self.magnitude = kwargs.get("magnitude", 0)
        self.place = kwargs.get("place", "")
        self.time = kwargs.get("time", 0)
        self._id = kwargs.get("id", "")
        self.coordinates = Coordinates(**kwargs.get("coordinates", {}))

    def __str__(self) -> str:
        return f"Magnitude: {self.magnitude}, Place: {self.place}, Time: {self.time}"

    def to_json(self) -> dict:
        return {
            "magnitude": self.magnitude,
            "place": self.place,
            "time": self.time,
            "coordinates": self.coordinates.to_json(),
        }

    def get_id(self) -> str:
        return self._id


class Coordinates:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.lon = kwargs.get("lon")
        self.lat = kwargs.get("lat")
        self.elevation = kwargs.get("elevation")

    def __str__(self) -> str:
        return f"Type:{self.type}, Lat:{self.lat}, Lon:{self.lon}, Elevation:{self.elevation}"

    def to_json(self) -> dict:
        return {
            "type": self.type,
            "lon": self.lon,
            "lat": self.lat,
            "elevation": self.elevation,
        }
