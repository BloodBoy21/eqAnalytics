from shared.db import db
from sqlalchemy import Column, Integer, String


class User(db):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    email = Column(String)
    country_code = Column(String, index=True)
    lat = Column(float)
    lon = Column(float)
