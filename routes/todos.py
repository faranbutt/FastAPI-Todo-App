import sys
sys.path.append('..')
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
from models import Base,Todos
from database import SessionLocal, engine
from sqlalchemy.orm import session,Session
from pydantic import BaseModel, Field
from routes.auth import get_current_user, get_user_exceptions
from routes import auth
router = APIRouter(prefix='/todos',tags=['todos'],responses={404:{"description":"Not found"}})
Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class TodoModel(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0,lt=6,description="The priority must be between 1-5")
    complete: bool

@router.get('/')
async def get_todos(db: session = Depends(get_db)):
    return db.query(Todos).all()


@router.get('/user')
async def read_all_from_user(user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    userData = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    
    return {"user":userData}


@router.get('/{todo_id}')
async def get_todo_by_id(todo_id:int,user:dict =  Depends(get_current_user), db: session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise Http_Exception()

@router.post('/')
async def create_todo(todo:TodoModel,user:dict = Depends(get_current_user) ,db:session = Depends(get_db)):
    todo_model = Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()

    return Successful_Response(201)

@router.put('/{todo_id}')
async def update_todo(todo_id:int, todo:TodoModel,user:dict = Depends(get_current_user), db:session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_model:Todos = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get("id")).first()
    if todo_model is None:
        raise Http_Exception()
    todo_model.title  = todo.title
    todo_model.description =  todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    return Successful_Response(200)

@router.delete('/{todo_id}')
async def delete_todo(todo_id:int,user:dict = Depends(get_current_user), db:session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise Http_Exception()
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

    return Successful_Response(201)


def Successful_Response(status_code:int):
    return {"status":status_code,
            "transaction":"Success"
            }

def Http_Exception():
    return HTTPException(status_code=404,detail='todo not found')