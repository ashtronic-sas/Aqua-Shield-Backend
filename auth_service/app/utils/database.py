from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://admin:LFS1ieqpA7bhuCK3W1Xo@db-aquashield-dev.c5guy4ya6433.us-east-2.rds.amazonaws.com:3306/dbaquashieldtest"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size= 10, max_overflow= 30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

