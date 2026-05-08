"""
Additional comprehensive tests for Event API endpoints.
"""
from fastapi.testclient import TestClient


def test_create_event_with_empty_name(client: TestClient):
	"""
	빈 이름으로 이벤트 생성이 허용되어야 한다.
	"""
	# Given: 빈 이름을 가진 이벤트 데이터
	event_data = {"name": ""}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created가 반환된다 (현재 빈 문자열 허용)
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == ""


def test_create_event_with_whitespace_only_name(client: TestClient):
	"""
	공백만 있는 이름으로 이벤트 생성 시 처리해야 한다.
	"""
	# Given: 공백만 있는 이름을 가진 이벤트 데이터
	event_data = {"name": "   "}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created가 반환되고 이름이 그대로 저장된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == "   "


def test_create_event_with_long_name(client: TestClient):
	"""
	긴 이름으로 이벤트 생성이 가능해야 한다.
	"""
	# Given: 매우 긴 이름을 가진 이벤트 데이터
	long_name = "매우 긴 이벤트 이름 " * 10  # 약 100자
	event_data = {"name": long_name}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created가 반환된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == long_name


def test_create_event_with_special_characters(client: TestClient):
	"""
	특수 문자가 포함된 이름으로 이벤트 생성이 가능해야 한다.
	"""
	# Given: 특수 문자가 포함된 이벤트 데이터
	event_data = {"name": "2025년 7월 회식 🍻 & 🍖 @ 강남역"}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created가 반환된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == "2025년 7월 회식 🍻 & 🍖 @ 강남역"


def test_create_event_with_numbers_only(client: TestClient):
	"""
	숫자만으로 이루어진 이름으로 이벤트 생성이 가능해야 한다.
	"""
	# Given: 숫자만 있는 이벤트 데이터
	event_data = {"name": "20250730"}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created가 반환된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == "20250730"


def test_create_event_with_invalid_json(client: TestClient):
	"""
	잘못된 JSON 형식으로 요청 시 실패해야 한다.
	"""
	# Given: 잘못된 JSON 데이터
	invalid_json = '{"name": "테스트"'  # 닫는 괄호 누락
	
	# When: POST /api/events 엔드포인트에 잘못된 JSON으로 요청을 보낸다
	response = client.post(
		"/api/events",
		data=invalid_json,
		headers={"Content-Type": "application/json"}
	)
	
	# Then: 422 Unprocessable Entity가 반환된다
	assert response.status_code == 422


def test_create_event_with_extra_fields(client: TestClient):
	"""
	추가 필드가 있는 요청도 정상 처리되어야 한다.
	"""
	# Given: 추가 필드가 있는 이벤트 데이터
	event_data = {
		"name": "테스트 이벤트",
		"description": "이 필드는 무시되어야 함",
		"extra_field": "추가 데이터"
	}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 Created가 반환되고 name만 저장된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == "테스트 이벤트"
	assert "description" not in response_data
	assert "extra_field" not in response_data


def test_get_events_after_creating_many(client: TestClient):
	"""
	많은 이벤트를 생성한 후 모든 이벤트를 조회할 수 있어야 한다.
	"""
	# Given: 10개의 이벤트를 생성한다
	event_names = [f"이벤트 {i}" for i in range(1, 11)]
	
	for name in event_names:
		response = client.post("/api/events", json={"name": name})
		assert response.status_code == 201
	
	# When: GET /api/events 엔드포인트에 요청을 보낸다
	response = client.get("/api/events")
	
	# Then: 200 OK와 모든 이벤트가 반환된다
	assert response.status_code == 200
	events = response.json()
	assert len(events) == 10
	
	# And: 이벤트들이 올바른 순서로 반환된다 (생성 순서)
	for i, event in enumerate(events):
		assert event["name"] == f"이벤트 {i + 1}"
		assert event["event_id"] == i + 1


def test_event_id_sequence(client: TestClient):
	"""
	이벤트 ID가 순차적으로 증가해야 한다.
	"""
	# Given: 여러 이벤트를 순차적으로 생성한다
	event_names = ["첫 번째", "두 번째", "세 번째"]
	created_ids = []
	
	# When: 각 이벤트를 생성하고 ID를 수집한다
	for name in event_names:
		response = client.post("/api/events", json={"name": name})
		assert response.status_code == 201
		created_ids.append(response.json()["event_id"])
	
	# Then: ID가 1부터 순차적으로 증가해야 한다
	assert created_ids == [1, 2, 3]


def test_get_events_returns_correct_structure(client: TestClient):
	"""
	이벤트 목록 조회 시 올바른 구조를 반환해야 한다.
	"""
	# Given: 이벤트를 하나 생성한다
	event_data = {"name": "구조 테스트 이벤트"}
	create_response = client.post("/api/events", json=event_data)
	assert create_response.status_code == 201
	
	# When: GET /api/events 엔드포인트에 요청을 보낸다
	response = client.get("/api/events")
	
	# Then: 올바른 구조의 응답이 반환된다
	assert response.status_code == 200
	events = response.json()
	assert len(events) == 1
	
	event = events[0]
	assert "event_id" in event
	assert "name" in event
	assert isinstance(event["event_id"], int)
	assert isinstance(event["name"], str)
	assert event["event_id"] > 0
	assert event["name"] == "구조 테스트 이벤트"


def test_api_endpoints_content_type(client: TestClient):
	"""
	API 엔드포인트들이 올바른 Content-Type을 반환해야 한다.
	"""
	# Given: 이벤트 데이터
	event_data = {"name": "Content-Type 테스트"}
	
	# When: POST 요청을 보낸다
	post_response = client.post("/api/events", json=event_data)
	
	# Then: 올바른 Content-Type이 반환된다
	assert post_response.status_code == 201
	assert "application/json" in post_response.headers.get("content-type", "")
	
	# When: GET 요청을 보낸다
	get_response = client.get("/api/events")
	
	# Then: 올바른 Content-Type이 반환된다
	assert get_response.status_code == 200
	assert "application/json" in get_response.headers.get("content-type", "")
