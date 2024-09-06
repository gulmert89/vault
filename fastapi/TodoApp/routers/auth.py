from models import Users
from starlette import status
from typing import Annotated
from pydantic import BaseModel
from jose import jwt, JWTError
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter(
    prefix="/auth",  # each endpoint in this file will start with this prefix
    tags=["auth"]
)  # app = FastAPI()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = "some_random_looooooooooooooooong_str"  # > openssl rand -hex 32
ALGORITHM = "HS256"

# Mert: I separate the exception as a variable to tidy things up.
http_exception_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user."
)


class CreateUserRequest(BaseModel):
    # "id" is omitted because SQLalchemy manages it automatically
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str
    # "is_active" is omitted because everytime we create a new user,
    # it'll be 'active' (True) by default.


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    """Creates a DB session."""
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print("Database error:", e)
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: db_dependency) -> bool:
    """
    Takes 'username' and 'password' and searches for the DB. If any related
    user is found, returns the 'user' object. Else, returns False.
    """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(secret=password, hash=user.hashed_password):
        # bcrypt will automatically hash the 'password' and match it.
        return False
    return user


def create_access_token(
        username: str,
        user_id: int,
        role: str,
        expires_delta: timedelta
) -> str:
    """Encodes the 'username' & 'user_id' and returns a JWT."""
    encode = {
        "sub": username,
        "id": user_id,
        "role": role
    }
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)


# observe that this is not an API endpoint
async def get_current_user(jwtoken: Annotated[str, Depends(oauth2_bearer)]):
    """
    Decodes a JWT and returns user data like 'username' & 'user_id'.
    """
    try:
        payload = jwt.decode(
            token=jwtoken,
            key=SECRET_KEY,
            algorithms=ALGORITHM
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise http_exception_401
        return {
            "username": username,
            "id": user_id,
            "role": user_role
        }
    except JWTError:
        raise http_exception_401


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest
) -> None:
    """
    Creates a user by instantiating an object of the Users class by
    providing various class variables coming from the request.
    Add the new user to the data base.
    """
    # create_user_model = Users(
    # **create_user_request.dict()
    # )  # This won't work because Users has 'hashed_password' but not
    # 'password'. Thus, we need to specify every arguments like this:
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        hashed_password=bcrypt_context.encrypt(create_user_request.password),
        is_active=True
    )
    # return create_user_model  # We don't return the model anymore. Instead,
    # we save the user to our database.
    db.add(create_user_model)
    db.commit()


@router.post(path="/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
) -> HTTPException | dict[str, str]:
    """
    Takes a form data which consists of user data, authenticates it and
     creates a token. Returns a dict of 'access_token' and 'token_type'.
    """
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db
    )
    if not user:
        raise http_exception_401
    token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=60)
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
