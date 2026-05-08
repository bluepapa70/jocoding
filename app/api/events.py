"""
Event API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.service.event_service import EventService
from app.service.menu_service import MenuService
from app.service.vote_service import VoteService
from app.schemas.event import EventCreate, EventResponse
from app.schemas.menu import MenuCreate, MenuResponse
from app.schemas.vote import VoteCreate, VoteResponse, VoteResult

router = APIRouter(prefix="/api", tags=["events"])


@router.post("/events", response_model=EventResponse, status_code=201)
def create_event(
	event_data: EventCreate,
	db: Session = Depends(get_db)
) -> EventResponse:
	"""Create a new dining event."""
	service = EventService(db)
	return service.create_event(event_data)


@router.get("/events", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)) -> List[EventResponse]:
	"""Get all dining events."""
	service = EventService(db)
	return service.get_all_events()


@router.post("/events/{event_id}/menus", response_model=MenuResponse, status_code=201)
def create_menu(
	event_id: int,
	menu_data: MenuCreate,
	db: Session = Depends(get_db)
) -> MenuResponse:
	"""Create a new menu candidate for an event."""
	service = MenuService(db)
	return service.create_menu(event_id, menu_data)


@router.get("/events/{event_id}/menus", response_model=List[MenuResponse])
def get_menus(
	event_id: int,
	db: Session = Depends(get_db)
) -> List[MenuResponse]:
	"""Get all menu candidates for an event."""
	service = MenuService(db)
	return service.get_menus_by_event(event_id)


@router.post("/events/{event_id}/votes", response_model=VoteResponse, status_code=201)
def create_vote(
	event_id: int,
	vote_data: VoteCreate,
	db: Session = Depends(get_db)
) -> VoteResponse:
	"""Create a vote for a menu candidate."""
	service = VoteService(db)
	return service.create_vote(event_id, vote_data)


@router.get("/events/{event_id}/results", response_model=List[VoteResult])
def get_vote_results(
	event_id: int,
	db: Session = Depends(get_db)
) -> List[VoteResult]:
	"""Get vote results for an event."""
	service = VoteService(db)
	return service.get_vote_results(event_id)
