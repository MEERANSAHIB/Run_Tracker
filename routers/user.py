from typing import Annotated
from pydantic import BaseModel,Field
from starlette import status
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import get_current_user, bcrypt_context
from models import Users, Runs

router=APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

class password_model(BaseModel):
    current_password:str
    new_password:str=Field(min_length=6)

@router.get("/information")
async def user_information(user:user_dependency,db:db_dependency):
    user_model=db.query(Users).filter(Users.id==user.get('user_id')).first()
    if user_model is None:
        raise HTTPException(status_code=404,detail="User does not exist")
    return user_model

@router.put("/change_password")
async def change_password(user:user_dependency,db:db_dependency,passwords:password_model):
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    if not bcrypt_context.verify(passwords.current_password,user_model.hashedpassword):
        raise HTTPException(status_code=401, detail="wrong password")
    new_hashed_password=bcrypt_context.hash(passwords.new_password)
    user_model.hashedpassword=new_hashed_password
    db.commit()

