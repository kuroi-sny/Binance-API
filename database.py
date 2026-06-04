from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

## URL to DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./trading_api.db"


## 1) Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

## Session local
SessionLocal = sessionmaker(bind=engine)

## Base 

Base = declarative_base()


## Bouncer to open the door

def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()





