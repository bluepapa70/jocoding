"""
Vote schemas for request/response validation.
"""
from pydantic import BaseModel


class VoteCreate(BaseModel):
	"""
	Schema for creating a new vote.
	
	Attributes:
		menu_id: ID of the menu to vote for
	"""
	menu_id: int


class VoteResponse(BaseModel):
	"""
	Schema for vote response.
	
	Attributes:
		vote_id: Unique identifier for the vote
		event_id: ID of the event this vote belongs to
		menu_id: ID of the menu that was voted for
	"""
	vote_id: int
	event_id: int
	menu_id: int
	
	model_config = {"from_attributes": True}


class VoteResult(BaseModel):
	"""
	Schema for vote result response.
	
	Attributes:
		menu_id: ID of the menu
		name: Name of the menu
		votes: Number of votes received
	"""
	menu_id: int
	name: str
	votes: int
