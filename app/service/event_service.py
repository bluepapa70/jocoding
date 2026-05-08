"""
Event service for business logic.
"""
from typing import List
from sqlalchemy.orm import Session

from app.repository.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse


class EventService:
	"""Service class for Event business logic."""
	
	def __init__(self, db: Session):
		"""
		Initialize the service with a database session.
		
		Args:
			db: SQLAlchemy database session
		"""
		self.repository = EventRepository(db)
	
	def create_event(self, event_data: EventCreate) -> EventResponse:
		"""
		Create a new event.
		
		Args:
			event_data: Event creation data
			
		Returns:
			Created event response
		"""
		db_event = self.repository.create_event(event_data)
		return EventResponse(event_id=int(db_event.id), name=str(db_event.name))
	
	def get_all_events(self) -> List[EventResponse]:
		"""
		Get all events.
		
		Returns:
			List of all events
		"""
		db_events = self.repository.get_all_events()
		return [
			EventResponse(event_id=int(event.id), name=str(event.name))
			for event in db_events
		]
