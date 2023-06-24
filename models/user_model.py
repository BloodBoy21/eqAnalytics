from shared.db import db
from sqlalchemy import Column, Integer, String, Float


class User(db):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    lat = Column(Float)
    lon = Column(Float)
