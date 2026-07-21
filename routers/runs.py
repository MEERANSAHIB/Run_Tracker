from typing import Annotated
from pydantic import BaseModel,Field
from starlette import status

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import get_current_user

from models import Users, Runs

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]



class createrun(BaseModel):
    title:str=Field(min_length=1)
    distance_km:float=Field(gt=0)
    duration_minutes:int=Field(gt=0)
    average_heart_rate:int=Field(gt=30,lt=260)
    
@router.post("/createnewrun",status_code=status.HTTP_201_CREATED)
async def createnewrun(user:user_dependency,db:db_dependency,newrun:createrun):
    if user is None:
        raise HTTPException(status_code=401,detail="Can't Authorize the user")
    newrun_model=Runs(**newrun.model_dump(),user_id=user.get('user_id'))
    db.add(newrun_model)
    db.commit()
@router.get("/getallruns")
async def getallruns(db:db_dependency):
    return db.query(Runs).all()
