"""
Vote repository for database operations.
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.vote import Vote
from app.models.menu import Menu
from app.schemas.vote import VoteCreate, VoteResult


class VoteRepository:
	"""Repository class for Vote database operations."""
	
	def __init__(self, db: Session):
		"""
		Initialize the repository with a database session.
		
		Args:
			db: SQLAlchemy database session
		"""
		self.db = db
	
	def create_vote(self, event_id: int, vote_data: VoteCreate) -> Vote:
		"""
		Create a new vote for a menu.
		
		Args:
			event_id: ID of the event
			vote_data: Vote creation data
			
		Returns:
			Created vote instance
		"""
		db_vote = Vote(event_id=event_id, menu_id=vote_data.menu_id)
		self.db.add(db_vote)
		self.db.commit()
		self.db.refresh(db_vote)
		return db_vote
	
	def get_vote_results(self, event_id: int) -> List[VoteResult]:
		"""
		Get vote results for a specific event.
		
		Args:
			event_id: ID of the event
			
		Returns:
			List of vote results with menu info and vote counts
		"""
		results = (
			self.db.query(
				Menu.id.label("menu_id"),
				Menu.name.label("name"),
				func.count(Vote.id).label("votes")
			)
			.outerjoin(Vote, Menu.id == Vote.menu_id)
			.filter(Menu.event_id == event_id)
			.group_by(Menu.id, Menu.name)
			.all()
		)
		
		return [
			VoteResult(menu_id=result.menu_id, name=result.name, votes=result.votes)
			for result in results
		]
