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

class run(BaseModel):
    id:int=Field(gt=0,lt=100)
    title: str = Field(min_length=1)
    distance_km: float = Field(gt=0)
    duration_minutes: int = Field(gt=0)
    average_heart_rate: int = Field(gt=30, lt=260)
    
@router.post("/createnewrun",status_code=status.HTTP_201_CREATED)
async def createnewrun(user:user_dependency,db:db_dependency,newrun:createrun):
    if user is None:
        raise HTTPException(status_code=401,detail="Can't Authorize the user")
    newrun_model=Runs(**newrun.model_dump(),user_id=user.get('user_id'))
    db.add(newrun_model)
    db.commit()
@router.get("/getallruns")
async def getallruns(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Can't Authorize the user")
    return db.query(Runs).filter(Runs.user_id==user.get('user_id')).all()

@router.get("/get_run_by_id/{run_id}")
async def get_run_by_id(user:user_dependency,db:db_dependency,run_id):
    if user is None:
        raise HTTPException(status_code=401, detail="Can't Authorize the user")
    run_model= db.query(Runs).filter(Runs.user_id==user.get('user_id'),Runs.id==run_id).first()
    if run_model is None:
        raise HTTPException(status_code=404,detail="run doesn't exist")
    return run_model

@router.put("/update_run")
async def update_run(user:user_dependency,db:db_dependency,updated_run:run):
    if user is None:
        raise HTTPException(status_code=401, detail="Can't Authorize the user")
    run_model= db.query(Runs).filter(Runs.user_id==user.get('user_id'),Runs.id==updated_run.id).first()
    run_model.title=updated_run.title
    run_model.distance_km=updated_run.distance_km
    run_model.duration_minutes=updated_run.duration_minutes
    run_model.average_heart_rate=updated_run.average_heart_rate

@router.delete("/delete_run/{run_id}")
async def delete_run(user:user_dependency,db:db_dependency,run_id):
    if user is None:
        raise HTTPException(status_code=401, detail="Can't Authorize the user")
    db.query(Runs).filter(Runs.id==run_id,Runs.user_id==user.get('id')).delete()
    db.commit()