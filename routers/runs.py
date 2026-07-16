from typing import Annotated
from pydantic import BaseModel,Field
from starlette import status

from database import SessionLocal
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



class createrun(BaseModel):
    title:str=Field(min_length=1)
    distance_km:float=Field(gt=0)
    duration_minutes:int=Field(gt=0)
    average_heart_rate:int=Field(gt=30,lt=260)
    user_id:int=Field(gt=0)
    
@router.post("/createnewrun",status_code=status.HTTP_201_CREATED)
async def createnewrun(newrun:createrun,db:db_dependency):
    newrun_model=Runs(**newrun.model_dump())
    db.add(newrun_model)
    db.commit()
@router.get("/getallruns")
async def getallruns(db:db_dependency):
    return db.query(Runs).all()
