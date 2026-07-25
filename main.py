from fastapi import FastAPI
from routers import runs, auth, admin, user
from database import Base,engine


app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(runs.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)