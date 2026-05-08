"""
Database configuration and setup.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
SQLITE_DATABASE_URL = "sqlite:///./app.db"

# Create engine
engine = create_engine(
	SQLITE_DATABASE_URL,
	connect_args={"check_same_thread": False}
)

# Create session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
	"""
	Database dependency for FastAPI.
	
	Yields:
		Database session that will be automatically closed.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def create_tables():
	"""Create all database tables."""
	Base.metadata.create_all(bind=engine)
