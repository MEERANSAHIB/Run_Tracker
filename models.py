from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from database import Base
class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    username=Column(String,unique=True,index=True)
    hashedpassword=Column(String)
    is_active=Column(Boolean)
    runs=Column(Integer)

class Runs(Base):
    __tablename__='runs'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    distance_km=Column(Float)
    duration_minutes=Column(Integer)
    average_heart_rate=Column(Integer)
    user_id=Column(Integer)
    owner=Column(Integer,ForeignKey(users.id))