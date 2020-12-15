"""
    CRUD endpoints for the API.
"""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from scraper.src import db as model


def get_vendings_latest(db: Session):
    latest = db.query(func.max(model.Vending.run_id)).one()[0]
    return db.query(model.Vending).filter(model.Vending.run_id == latest).all()

def get_vendings_timerange(db: Session, dt_start: datetime, dt_end: datetime):
    return (db.query(model.Vending)
            .filter(model.Vending.created_at >= dt_start)
            .filter(model.Vending.created_at <= dt_end)
            .all())

def get_item(db: Session, item_id: int):
    return db.query(model.VendingEntry).filter(model.VendingEntry.item_id == item_id).all()
