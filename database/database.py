# Import necessary attributes from SQLAlchemy
from sqlalchemy import String
from sqlalchemy import MetaData

# Import necessary modules for creating a connection to the database
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///storage.db"

# Creating an engine
engine = create_engine(DATABASE_URL, echo=True)

# Base used for models
Base = declarative_base()

# For database connectivity
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()
