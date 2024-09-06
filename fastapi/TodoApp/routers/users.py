from models import Users
from typing import Annotated
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, bcrypt_context
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


class UserRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


def get_db():
    """Creates a DB session."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print("Database error:", e)
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
http_exception_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user."
)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def get_user_data(user: user_dependency, db: db_dependency):
    if user is None:
        raise http_exception_401
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put(path="/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_request: UserRequest
):
    if user is None:
        raise http_exception_401
    curr_user = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(
        secret=user_request.old_password,
        hash=curr_user.hashed_password
    ):
        raise http_exception_401
    new_passw = bcrypt_context.encrypt(user_request.new_password)
    curr_user.hashed_password = new_passw
    db.add(curr_user)
    db.commit()
