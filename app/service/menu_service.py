"""
Menu service for business logic.
"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.menu_repository import MenuRepository
from app.repository.event_repository import EventRepository
from app.schemas.menu import MenuCreate, MenuResponse


class MenuService:
	"""Service class for Menu business logic."""
	
	def __init__(self, db: Session):
		"""
		Initialize the service with a database session.
		
		Args:
			db: SQLAlchemy database session
		"""
		self.menu_repository = MenuRepository(db)
		self.event_repository = EventRepository(db)
	
	def create_menu(self, event_id: int, menu_data: MenuCreate) -> MenuResponse:
		"""
		Create a new menu candidate for an event.
		
		Args:
			event_id: ID of the event
			menu_data: Menu creation data
			
		Returns:
			Created menu response
			
		Raises:
			HTTPException: If the event does not exist
		"""
		# Verify event exists
		events = self.event_repository.get_all_events()
		event_exists = any(event.id == event_id for event in events)
		if not event_exists:
			raise HTTPException(status_code=404, detail="Event not found")
		
		db_menu = self.menu_repository.create_menu(event_id, menu_data)
		return MenuResponse(
			id=int(db_menu.id), 
			event_id=int(db_menu.event_id), 
			name=str(db_menu.name)
		)
	
	def get_menus_by_event(self, event_id: int) -> List[MenuResponse]:
		"""
		Get all menu candidates for an event.
		
		Args:
			event_id: ID of the event
			
		Returns:
			List of menu responses
			
		Raises:
			HTTPException: If the event does not exist
		"""
		# Verify event exists
		events = self.event_repository.get_all_events()
		event_exists = any(event.id == event_id for event in events)
		if not event_exists:
			raise HTTPException(status_code=404, detail="Event not found")
		
		db_menus = self.menu_repository.get_menus_by_event(event_id)
		return [
			MenuResponse(
				id=int(menu.id), 
				event_id=int(menu.event_id), 
				name=str(menu.name)
			)
			for menu in db_menus
		]
