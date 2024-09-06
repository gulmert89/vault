from models import Todos
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status, Path


router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)


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
no_todo_exception = HTTPException(
            status_code=404,
            detail="The requested todo couldn't be found."
)
http_exception_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user."
)


class TodoRequest(BaseModel):
    # we don't need to pass the `id` field since it's the primary key
    # in the Todos class. User doesn't need to know what id will be used.
    # sqlalchemy does the id increment for us.
    title: str = Field(min_length=1)
    description: str = Field(min_length=2, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user:
        raise http_exception_401
    user_id_fetched = user.get("id")
    print("[TODOS-INFO] All todos are fetch for user ID:", user_id_fetched)
    return db.query(Todos).filter(Todos.owner_id == user_id_fetched).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
):
    if user is None:
        raise http_exception_401
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id"))\
        .filter(Todos.id == todo_id).first()
    # .first() is to speed up the process since the code doesn't know
    # how many ids we have.
    if todo_model is not None:
        return todo_model
    else:
        raise no_todo_exception


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest
) -> None:
 
    todo_model = Todos(**todo_request.dict(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0)
) -> None:
    if user is None:
        raise http_exception_401
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id"))\
        .filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise no_todo_exception
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    # sqlalchemy will know that we are not creating a new todo but changing
    # the current one. Thus, there will be no duplicate or new todo when we
    # update the todo of which we provide the id.
    db.add(todo_model)
    db.commit()


@router.delete(path="/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
) -> None:
    if user is None:
        raise http_exception_401
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id"))\
        .filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise no_todo_exception
    db.query(Todos).filter(Todos.owner_id == user.get("id"))\
        .filter(Todos.id == todo_id).delete()
    db.commit()
