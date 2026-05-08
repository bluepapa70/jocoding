"""
This module initializes and configures the FastAPI application for the 회식 메뉴 투표 API (Company Dinner Menu Voting API).
It sets up the application lifespan events, includes API routers, and provides a root endpoint for health checks.
Key Components:
- Lifespan event handler: Manages startup and shutdown events, including database table creation.
- FastAPI app instance: Configured with metadata such as title, description, and version.
- Router inclusion: Registers API routes from the events module.
- Root endpoint: Provides a simple health check response.
Modules Imported:
- contextlib.asynccontextmanager: For managing application lifespan events asynchronously.
- fastapi.FastAPI: The main FastAPI application class.
- app.api.events: Contains API route definitions.
- app.models.database.create_tables: Function to initialize database tables.
Main FastAPI application.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import events, comment
from app.models.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Lifespan event handler for application startup and shutdown."""
	# Startup
	create_tables()
	yield
	# Shutdown (if needed)


# Create FastAPI app instance
app = FastAPI(
	title="회식 메뉴 투표 API",
	description="회식 이벤트별 메뉴 투표 백엔드 API",
	version="1.0.0",
	lifespan=lifespan
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

# Include routers
app.include_router(events.router)
app.include_router(comment.router)


@app.get("/")
def root():
	"""Root endpoint for health check."""
	return {"message": "회식 메뉴 투표 API 서버가 실행 중입니다."}
