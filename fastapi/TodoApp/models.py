from database import Base
from sqlalchemy import Boolean, Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(type_=Integer, primary_key=True, index=True)
    email = Column(type_=String, unique=True)
    username = Column(type_=String, unique=True)
    first_name = Column(type_=String, unique=False)
    last_name = Column(type_=String)
    hashed_password = Column(type_=String)
    is_active = Column(type_=Boolean, default=True)
    role = Column(type_=String)
    phone_number = Column(type_=String)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)

    todos = relationship("Todos", back_populates="owner")
    address = relationship("Address", back_populates="user_address")


class Todos(Base):
    __tablename__ = "todos"

    id = Column(type_=Integer, primary_key=True, index=True)
    title = Column(type_=String)
    description = Column(type_=String)
    priority = Column(type_=Integer)
    complete = Column(type_=Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Which argument does ForeignKey refers to ffs?

    owner = relationship("Users", back_populates="todos")


class Address(Base):
    __tablename__ = "address"

    id = Column(type_=Integer, primary_key=True, index=True)
    address1 = Column(type_=String)
    address2 = Column(type_=String)
    apt_num = Column(type_=String)
    city = Column(type_=String)
    state = Column(type_=String)
    country = Column(type_=String)
    postalcode = Column(type_=String)

    user_address = relationship("Users", back_populates="address")
