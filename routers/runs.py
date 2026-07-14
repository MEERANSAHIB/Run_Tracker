from typing import Annotated

from pydantic import BaseModel
from pydantic.v1 import Field

from database import Base, SessionLocal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Users, Runs

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

class usercreate(BaseModel):
    email:str
    username:str
    hashedpassword:str

@router.post("/createnewuser")
async def createnewuser(newuser:usercreate,db:db_dependency):
    newusermodel=Users(**newuser.model_dump())
    db.add(newusermodel)
    db.commit()

@router.get("/getallusers")
async def getallusers(db:db_dependency):
    return db.query(Users).all()

class createrun(BaseModel):
    title:str=Field(min_length=1)
    distance_km:float=Field(gt=0.5)
    duration_minutes:int=Field(gt=0.5)
    average_heart_rate:int=Field(gt=30,lt=260)
    user_id:int=Field(gt=0)
    
@router.post("/createnewrun")
async def createnewrun(newrun:createrun,db:db_dependency):
    newrun_model=Runs(**newrun.model_dump())
    db.add(newrun_model)
    db.commit()
@router.get("/getallruns")
async def getallruns(db:db_dependency):
    return db.query(Runs).all()
