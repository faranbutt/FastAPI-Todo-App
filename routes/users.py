import sys
sys.path.append("..")

from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from models import Base,Users
from pydantic import BaseModel
from routes.auth import get_current_user, verify_password
import binascii
from bcrypt import hashpw,gensalt


router =  APIRouter(prefix='/users',tags=['users'],responses={404:{'deescription':"Not found"}})

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def getPasswordHash(password):
    return hashpw(password,gensalt())

class UserVerification(BaseModel):
    username: str
    password: str
    newPassword: str

@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(Users).all()

#user by query
@router.get('/user')
async def get_user_by_name(username: str,db:Session = Depends(get_db)):
    user  = db.query(Users).filter(Users.username == username).first()
    if user is None:
        raise get_user_exceptions()
    return user
#user by path
@router.get('/{user_id}')
async def get_user_by_id(user_id:int ,db:Session=Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise get_user_exceptions()
    return user
@router.put('/user/password')
async def update_user_password(user_verification:UserVerification,user:dict = Depends(get_current_user),db:Session = Depends(get_db)) :
    if user is None:
        raise get_user_exceptions()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is not None:
        en_Pw = binascii.unhexlify(user_model.hased_password[2:])
        if user_verification.username == user_model.username and verify_password(user_verification.password.encode("utf-8"),en_Pw):
            user_model.hased_password = getPasswordHash(user_verification.newPassword.encode("utf-8"))
            db.add(user_model)
            db.commit()
            return 'successfull'
    return "invalid User or Request"

@router.delete('/user')
async def delete_user(user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        return "Invalid user or request"
    
    db.query(Users).filter(Users.id == user.get("id")).delete()
    db.commit()
    return "User is Deleted"


def get_user_exceptions():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Could not validate Credentials',headers={"WWW-Authenticate":"Bearer"})

