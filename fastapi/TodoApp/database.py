from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# After Notes 2.5: We are not connecting to our sqlite3 db anymore.
# You can delete (well, I won't) todos_app.db now.
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:50504648@localhost/TodoAppDB"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:50504648@127.0.0.1:3306/TodoAppDB"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    # connect_args={  # this parameter is for sqlite3 only
    #     "check_same_thread": False  # b.c there could be multiple threats
    # }
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
# Base will allow us to create each database models,
# which we will inherit later.
Base = declarative_base()
