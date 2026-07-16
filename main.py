from fastapi import FastAPI
from routers import runs, auth
from database import Base,engine


app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(runs.router)
app.include_router(auth.router)