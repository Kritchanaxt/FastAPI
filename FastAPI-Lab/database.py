
# import SQL Alchemy 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Run .env
from dotenv import load_dotenv

load_dotenv()

#? Step 1: Create a Alchemy engine

#* No used .env
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#* used .env 
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()