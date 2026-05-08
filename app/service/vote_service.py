"""
Vote service for business logic.
"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.vote_repository import VoteRepository
from app.repository.menu_repository import MenuRepository
from app.repository.event_repository import EventRepository
from app.schemas.vote import VoteCreate, VoteResponse, VoteResult


class VoteService:
	"""Service class for Vote business logic."""
	
	def __init__(self, db: Session):
		"""
		Initialize the service with a database session.
		
		Args:
			db: SQLAlchemy database session
		"""
		self.vote_repository = VoteRepository(db)
		self.menu_repository = MenuRepository(db)
		self.event_repository = EventRepository(db)
	
	def create_vote(self, event_id: int, vote_data: VoteCreate) -> VoteResponse:
		"""
		Create a new vote for a menu.
		
		Args:
			event_id: ID of the event
			vote_data: Vote creation data
			
		Returns:
			Created vote response
			
		Raises:
			HTTPException: If the event or menu does not exist or menu doesn't belong to event
		"""
		# Verify event exists
		events = self.event_repository.get_all_events()
		event_exists = any(event.id == event_id for event in events)
		if not event_exists:
			raise HTTPException(status_code=404, detail="Event not found")
		
		# Verify menu exists and belongs to the event
		menu = self.menu_repository.get_menu_by_id(vote_data.menu_id)
		if not menu:
			raise HTTPException(status_code=404, detail="Menu not found")
		
		if menu.event_id != event_id:
			raise HTTPException(status_code=400, detail="Menu does not belong to this event")
		
		db_vote = self.vote_repository.create_vote(event_id, vote_data)
		return VoteResponse(
			vote_id=int(db_vote.id),
			event_id=int(db_vote.event_id),
			menu_id=int(db_vote.menu_id)
		)
	
	def get_vote_results(self, event_id: int) -> List[VoteResult]:
		"""
		Get vote results for an event.
		
		Args:
			event_id: ID of the event
			
		Returns:
			List of vote results
			
		Raises:
			HTTPException: If the event does not exist
		"""
		# Verify event exists
		events = self.event_repository.get_all_events()
		event_exists = any(event.id == event_id for event in events)
		if not event_exists:
			raise HTTPException(status_code=404, detail="Event not found")
		
		return self.vote_repository.get_vote_results(event_id)
