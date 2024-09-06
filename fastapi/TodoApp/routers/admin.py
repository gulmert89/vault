from models import Todos
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status, Path


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print("Database error:", e)
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
no_todo_exception = HTTPException(
            status_code=404,
            detail="The requested todo couldn't be found."
)
http_exception_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user."
)


@router.get(path="/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") != "admin":
        raise http_exception_401
    return db.query(Todos).all()


@router.delete(path="/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
) -> None:
    if user is None or user.get("role") != "admin":
        raise http_exception_401
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise no_todo_exception
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
