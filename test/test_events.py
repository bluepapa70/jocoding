"""
Tests for event API endpoints.
"""
from fastapi.testclient import TestClient


def test_create_event_success(client: TestClient):
	"""
	새로운 이벤트를 성공적으로 생성해야 한다.
	"""
	# Given: 이벤트 생성 데이터
	event_data = {"name": "2025년 7월 회식"}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created와 이벤트 정보가 반환된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["event_id"] == 1
	assert response_data["name"] == "2025년 7월 회식"


def test_create_event_invalid_data(client: TestClient):
	"""
	잘못된 데이터로 이벤트 생성 시 실패해야 한다.
	"""
	# Given: 잘못된 이벤트 데이터 (name 필드 누락)
	event_data = {}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 422 Unprocessable Entity가 반환된다
	assert response.status_code == 422


def test_get_events_empty(client: TestClient):
	"""
	이벤트가 없을 때 빈 리스트를 반환해야 한다.
	"""
	# Given: 데이터베이스에 이벤트가 없는 상태
	
	# When: GET /api/events 엔드포인트에 요청을 보낸다
	response = client.get("/api/events")
	
	# Then: 200 OK와 빈 리스트가 반환된다
	assert response.status_code == 200
	assert response.json() == []


def test_get_events_with_data(client: TestClient):
	"""
	이벤트가 있을 때 이벤트 목록을 반환해야 한다.
	"""
	# Given: 두 개의 이벤트를 생성한다
	event1_data = {"name": "2025년 7월 회식"}
	event2_data = {"name": "2025년 8월 회식"}
	
	client.post("/api/events", json=event1_data)
	client.post("/api/events", json=event2_data)
	
	# When: GET /api/events 엔드포인트에 요청을 보낸다
	response = client.get("/api/events")
	
	# Then: 200 OK와 이벤트 목록이 반환된다
	assert response.status_code == 200
	events = response.json()
	assert len(events) == 2
	assert events[0]["name"] == "2025년 7월 회식"
	assert events[1]["name"] == "2025년 8월 회식"


def test_create_multiple_events(client: TestClient):
	"""
	여러 이벤트를 생성할 수 있어야 한다.
	"""
	# Given: 여러 이벤트 데이터
	events_data = [
		{"name": "팀 회식"},
		{"name": "부서 회식"},
		{"name": "전사 회식"}
	]
	
	# When: 각 이벤트를 생성한다
	created_events = []
	for event_data in events_data:
		response = client.post("/api/events", json=event_data)
		assert response.status_code == 201
		created_events.append(response.json())
	
	# Then: 각 이벤트가 고유한 ID를 가져야 한다
	event_ids = [event["event_id"] for event in created_events]
	assert len(set(event_ids)) == len(event_ids)  # 모든 ID가 고유해야 함
	
	# And: 모든 이벤트를 조회할 수 있어야 한다
	response = client.get("/api/events")
	assert response.status_code == 200
	events = response.json()
	assert len(events) == 3
