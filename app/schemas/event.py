"""
Event schemas for request/response validation.
"""
from pydantic import BaseModel


class EventCreate(BaseModel):
	"""
	Schema for creating a new event.
	
	Attributes:
		name: Name of the event
	"""
	name: str


class EventResponse(BaseModel):
	"""
	Schema for event response.
	
	Attributes:
		event_id: Unique identifier for the event
		name: Name of the event
	"""
	event_id: int
	name: str
	
	model_config = {"from_attributes": True}
