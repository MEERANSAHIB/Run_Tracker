from typing import Annotated
from pydantic import BaseModel,Field
from starlette import status
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import Users, Runs

router=APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get("/get_runs_of_every_users",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency,user:user_dependency):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Runs).all()

@router.delete('/to_delete_runs_as_a_admin/{run_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_run(db:db_dependency,user:user_dependency,run_id):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=401,detail="Authentication Failed")
    run_model=db.query(Runs).filter(Runs.id==run_id).first()
    if run_model is None:
        raise HTTPException(status_code=404,detail="Run with given id can't be found")
    db.query(Runs).filter(Runs.id==run_id).delete()
    db.commit()