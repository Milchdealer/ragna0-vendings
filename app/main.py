"""
    API providing the ragna0 vending info.
"""
import os
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from scraper.src.db import Vending, VendingEntry
from api import crud, schema

SQLITE_DB = os.getenv("RAGNA0_SQLITE_PATH", "/data/ragna0.db")

engine = create_engine(
    "sqlite:///%s" % SQLITE_DB, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=List[schema.Vending])
def get_vendings_latest(db: Session = Depends(get_db)):
   vendings = crud.get_vendings_latest(db)
   return vendings

@app.get("/item/{item_id}", response_model=List[schema.VendingEntry])
def get_item_stats(item_id: int, db: Session = Depends(get_db)):
    item_entries = crud.get_item(db, item_id)
    return item_entries
