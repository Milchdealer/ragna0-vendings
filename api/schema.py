"""
    Pydantic schemas for database models.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class VendingEntryBase(BaseModel):
    id: int
    vending_id: int
    item_id: int
    name: str
    refine: Optional[int] = None
    slot: Optional[str] = None
    card0: Optional[str] = None
    card1: Optional[str] = None
    card2: Optional[str] = None
    card3: Optional[str] = None
    option0: Optional[str] = None
    option1: Optional[str] = None
    option2: Optional[str] = None
    option3: Optional[str] = None
    option4: Optional[str] = None
    price: int
    amount: int

    class Config:
        orm_mode = True


class VendingBase(BaseModel):
    id: int
    v_id: int
    v_name: str
    title: str
    m: str
    x: int
    y: int
    gender: str
    run_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Vending(VendingBase):
    items: List[VendingEntryBase] = []

    class Config:
        orm_mode = True


class VendingEntry(VendingEntryBase):
    shop: VendingBase = []

    class Config:
        orm_mode = True
