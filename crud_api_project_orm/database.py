from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@<postgresserver ipaddress or hostname>/<database name>"
# We are having default "postgres" user in our database, so using that.
#Database name for our project is "fastapi_orm"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine( SQLALCHEMY_DATABASE_URL )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
