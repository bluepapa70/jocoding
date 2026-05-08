"""
Vote database model.
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.database import Base


class Vote(Base):
	"""
	Vote model for storing vote information.
	
	Attributes:
		id: Primary key, auto-incrementing integer
		event_id: Foreign key referencing the event
		menu_id: Foreign key referencing the menu
		event: Relationship to the Event model
		menu: Relationship to the Menu model
	"""
	__tablename__ = "votes"
	
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
	menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
	
	# Relationships
	event = relationship("Event", back_populates="votes")
	menu = relationship("Menu", back_populates="votes")
