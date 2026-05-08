"""
Menu database model.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.database import Base


class Menu(Base):
	"""
	Menu model for storing menu candidate information.
	
	Attributes:
		id: Primary key, auto-incrementing integer
		event_id: Foreign key referencing the event
		name: Name of the menu candidate, required string
		event: Relationship to the Event model
		votes: Relationship to Vote models
	"""
	__tablename__ = "menus"
	
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
	name = Column(String, nullable=False)
	
	# Relationships
	event = relationship("Event", back_populates="menus")
	votes = relationship("Vote", back_populates="menu")
