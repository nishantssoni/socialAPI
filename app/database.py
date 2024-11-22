from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

# loading the .env file
load_dotenv()
DB_HOST = os.getenv("HOST")
DB_NAME = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("PASSWORD")


# Construct database URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DB_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()