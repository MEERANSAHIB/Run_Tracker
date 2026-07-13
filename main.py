from fastapi import FastAPI
from sqlalchemy import engine

app=FastAPI()
Base.metadata.create_all(bind=engine)