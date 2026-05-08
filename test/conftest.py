"""
Test configuration and fixtures for the application.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.database import Base, get_db
from app.main import app


# Create test database engine
SQLITE_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
	SQLITE_DATABASE_URL,
	connect_args={
		"check_same_thread": False,
	},
	poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
	"""Override database dependency for testing."""
	try:
		db = TestingSessionLocal()
		yield db
	finally:
		db.close()


@pytest.fixture(autouse=True)
def setup_database():
	"""Create and clean up test database for each test."""
	# Create all tables
	Base.metadata.create_all(bind=engine)
	yield
	# Drop all tables after test
	Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
	"""Create test client with overridden database dependency."""
	app.dependency_overrides[get_db] = override_get_db
	with TestClient(app) as test_client:
		yield test_client
	app.dependency_overrides.clear()
