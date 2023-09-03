from sqlalchemy import Boolean,Column,Integer,String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    hased_password = Column(String)
    is_active = Column(Boolean)
    phone_number = Column(String)
    # address_id = Column(Integer,ForeignKey("address_id"),nullable=True)
    todos = relationship("Todos",back_populates="owner")
    # address = relationship("Address",back_populates='user_address')



class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer,ForeignKey('users.id'))
    owner =relationship("Users",back_populates="todos")

# class Address(Base):
#     __tablename__='address'
#     id = Column(Integer,primary_key=True,index=True)
#     address1 = Column(String)
#     address2 = Column(String)
#     city = Column(String)
#     state = Column(String)
#     country = Column(String)
#     postalcode = Column(String)
#     user_address = relationship('Users',back_populates="address")