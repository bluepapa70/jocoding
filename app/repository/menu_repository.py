"""
Menu repository for database operations.
"""
from typing import List
from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.schemas.menu import MenuCreate


class MenuRepository:
	"""Repository class for Menu database operations."""
	
	def __init__(self, db: Session):
		"""
		Initialize the repository with a database session.
		
		Args:
			db: SQLAlchemy database session
		"""
		self.db = db
	
	def create_menu(self, event_id: int, menu_data: MenuCreate) -> Menu:
		"""
		Create a new menu candidate for an event.
		
		Args:
			event_id: ID of the event
			menu_data: Menu creation data
			
		Returns:
			Created menu instance
		"""
		db_menu = Menu(event_id=event_id, name=menu_data.name)
		self.db.add(db_menu)
		self.db.commit()
		self.db.refresh(db_menu)
		return db_menu
	
	def get_menus_by_event(self, event_id: int) -> List[Menu]:
		"""
		Get all menu candidates for a specific event.
		
		Args:
			event_id: ID of the event
			
		Returns:
			List of menu candidates for the event
		"""
		return self.db.query(Menu).filter(Menu.event_id == event_id).all()
	
	def get_menu_by_id(self, menu_id: int) -> Menu | None:
		"""
		Get a menu by its ID.
		
		Args:
			menu_id: ID of the menu
			
		Returns:
			Menu instance if found, None otherwise
		"""
		return self.db.query(Menu).filter(Menu.id == menu_id).first()
