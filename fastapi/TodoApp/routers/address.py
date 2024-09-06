import sys
sys.path.append("...")

import models
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from database import engine, SessionLocal
from .auth import get_current_user, http_exception_401


router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={
        404: {
                "description": "Not found."
        }
    }
)


def get_db():
    """Creates a DB session."""
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print("Database error:", e)
    finally:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    apt_num: Optional[int]
    city: str
    state: str
    country: str
    postalcode: str


@router.post("/")
async def create_address(
    address: Address,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user is None:
        raise http_exception_401
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.apt_num = address.apt_num
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()  # Flush all the object changes to the database.

    user_model = db.query(models.Users).filter(
        models.Users.id == user.get("id")
    ).first()
    user_model.address_id = address_model.id

    db.add(user_model)
    db.commit()  # Flush pending changes and commit the current transaction
