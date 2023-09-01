from fastapi import FastAPI, Depends, HTTPException
from models import Base
from database import SessionLocal, engine
from routes import auth, todos, users,address
from company import companyapis,dependencies
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router,prefix='/companyapis',tags=['company apis'],dependencies=[Depends(dependencies.get_token_header)],responses={418:{"description":"Internal data"}})
app.include_router(users.router)
app.include_router(address.route)