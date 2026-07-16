from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from starlette import status

from database import SessionLocal
from models import Users

router=APIRouter(
    prefix="/auth",
    tags=['auth']
)

SECRET_KEY="9f4c2e7a81d5b3c6a0f9e4b72c1d8a5f"
ALGORITHM="HS256"
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
OAuth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
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
    password:str

class token(BaseModel):
    access_token:str
    token_type:str

@router.post("/createnewuser")
async def createnewuser(newuser:usercreate,db:db_dependency):
    newusermodel=Users(
        email=newuser.email,
        username=newuser.username,
        hashedpassword=bcrypt_context.hash(newuser.password)
    )
    db.add(newusermodel)
    db.commit()

@router.get("/getallusers")
async def getallusers(db:db_dependency):
    return db.query(Users).all()

def validate_user(username,password,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashedpassword):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:timedelta):

    encode={'sub':username,'id':user_id}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(OAuth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str  = payload.get('sub')
        user_id:int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='could not verify user')
        return {'username':username,'user_id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='could not verify user')


@router.post("/userlogin",response_model=token)
async def userlogin(new_form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    if validate_user(new_form.username,new_form.password,db):
        user =db.query(Users).filter(Users.username==new_form.username).first()
        token=create_access_token(user.username,user.id,timedelta(minutes=20))
        return {"access_token":token,"token_type":"bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='could not verify user')