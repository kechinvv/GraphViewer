from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models import Base

print(os.getenv('db_conn'))
engine = create_engine(os.getenv('db_conn'), echo=True)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
