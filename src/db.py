"""
	Database models for vending shops.
"""
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vending(Base):
	__tablename__ = "vendings"

	id = Column(Integer, primary_key=True)
	v_id = Column(Integer)
	v_name = Column(String)
	title = Column(String)
	m = Column(String)
	x = Column(Integer)
	y = Column(Integer)
	gender = Column(String)

	created_at = Column(DateTime, default=datetime.utcnow)

class VendingEntry(Base):
	__tablename__ = "vending_entries"

	id = Column(Integer, primary_key=True)
	vending_id = Column(Integer, ForeignKey("vendings.id"))
	item_id = Column(Integer)
	name = Column(String)
	refine = Column(Integer)
	slot = Column(Integer)
	card0 = Column(String)
	card1 = Column(String)
	card2 = Column(String)
	card3 = Column(String)
	option0 = Column(String)
	option1 = Column(String)
	option2 = Column(String)	
	option3 = Column(String)
	option4 = Column(String)
	price = Column(Integer)
	amount = Column(Integer)
