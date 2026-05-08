"""
Event repository for database operations.
"""
from typing import List
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate


class EventRepository:
	"""Repository class for Event database operations."""
	
	def __init__(self, db: Session):
		"""
		Initialize the repository with a database session.
		
		Args:
			db: SQLAlchemy database session
		"""
		self.db = db
	
	def create_event(self, event_data: EventCreate) -> Event:
		"""
		Create a new event in the database.
		
		Args:
			event_data: Event creation data
			
		Returns:
			Created event instance
		"""
		db_event = Event(name=event_data.name)
		self.db.add(db_event)
		self.db.commit()
		self.db.refresh(db_event)
		return db_event
	
	def get_all_events(self) -> List[Event]:
		"""
		Get all events from the database.
		
		Returns:
			List of all events
		"""
		return self.db.query(Event).all()
