import models
from database import engine
from fastapi import FastAPI
# router imports
from routers import auth, todos, admin, users, address


app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(address.router)
models.Base.metadata.create_all(
    bind=engine
)  # Creates everything from database.py & models.py files.
# So we have created a DB without writing any SQL code.
