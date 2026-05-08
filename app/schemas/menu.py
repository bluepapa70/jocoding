"""
Menu schemas for request/response validation.
"""
from pydantic import BaseModel


class MenuCreate(BaseModel):
	"""
	Schema for creating a new menu candidate.
	
	Attributes:
		name: Name of the menu candidate
	"""
	name: str


class MenuResponse(BaseModel):
	"""
	Schema for menu response.
	
	Attributes:
		id: Unique identifier for the menu
		event_id: ID of the event this menu belongs to
		name: Name of the menu candidate
	"""
	id: int
	event_id: int
	name: str
	
	model_config = {"from_attributes": True}
