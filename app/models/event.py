"""
Event database model.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class Event(Base):
	"""
	Event model for storing dining event information.
	
	Attributes:
		id: Primary key, auto-incrementing integer
		name: Name of the event, required string
		menus: Relationship to Menu models
		votes: Relationship to Vote models
	"""
	__tablename__ = "events"
	
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	name = Column(String, nullable=False)
	
	# Relationships
	menus = relationship("Menu", back_populates="event")
	votes = relationship("Vote", back_populates="event")
