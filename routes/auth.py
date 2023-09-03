import sys
sys.path.append('..')

from fastapi import Depends, HTTPException,status, APIRouter
from  models import Base,Users
from pydantic import BaseModel
from typing import Optional
import bcrypt
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
import binascii

SECRET_KEY = "Faran is a hacker"
ALGORITHM = 'HS256'

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str
    phone_number: str

router = APIRouter(prefix='/auth',tags=['auth'],responses={404:{"description":"User not Authorized"}})

Base.metadata.create_all(bind=engine)

oauth2_bearer =  OAuth2AuthorizationCodeBearer(tokenUrl="token",authorizationUrl="token")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def verify_password(plainPassword:str,hashedPassword:str):
    
    return bcrypt.checkpw(plainPassword,hashedPassword)

def authenticate_user(username:str,password:str,db:Session):
    user = db.query(Users).filter(Users.username == username).first()
    print(user.hased_password[2:])
    en_Pw = binascii.unhexlify(user.hased_password[2:])
    
    if not user:
        return False
    if not verify_password(password.encode("utf-8"),en_Pw):
        return False
    return user


def create_access_token(username:str,user_id:int,expires_delta:Optional[timedelta]):
    encode = {"sub":username,"id":user_id}
    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=15)
    
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,ALGORITHM)

async def get_current_user(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        if username is None or user_id is None :
            raise get_user_exceptions()
        return {"username":username,"id":user_id}
    except JWTError:
        raise token_exceptions()


@router.post('/create/user')
async def create_new_user(create_user: CreateUser, db:Session = Depends(get_db)):
    create_user_model = Users()
    create_user_model.username = create_user.username
    create_user_model.email = create_user.email
    create_user_model.firstname = create_user.firstname
    create_user_model.lastname = create_user.lastname
    hashedPassword=bcrypt.hashpw((create_user.password.encode('utf-8')),bcrypt.gensalt(rounds=15))
    create_user_model.hased_password = hashedPassword
    create_user_model.is_active = True
    create_user_model.phone_number = create_user.phone_number
    user =  db.query(Users).filter(Users.email == create_user_model.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User Already exists')
    
    db.add(create_user_model)
    db.commit()
    return {"status":200,"transaction":"Success"}


@router.post('/token')
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = authenticate_user(form.username,form.password,db)
    if not user:
        raise get_user_exceptions()
    
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,user.id,expires_delta=token_expires)
    return {"token":token}

#Exceptions

def get_user_exceptions():
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate Credentials',headers={"WWW-Authenticate":"Bearer"})
    return credentials_exception

def token_exceptions():

    token_exception_response = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",headers={"WWW-Authenticate":"Bearer"})
    return token_exception_response