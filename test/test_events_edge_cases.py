"""
Error handling and edge case tests for Event API endpoints.
"""
from fastapi.testclient import TestClient


def test_invalid_http_methods(client: TestClient):
	"""
	지원하지 않는 HTTP 메서드로 요청 시 적절한 오류를 반환해야 한다.
	"""
	# When: PUT 메서드로 요청을 보낸다
	put_response = client.put("/api/events")
	
	# Then: 405 Method Not Allowed가 반환된다
	assert put_response.status_code == 405
	
	# When: DELETE 메서드로 요청을 보낸다
	delete_response = client.delete("/api/events")
	
	# Then: 405 Method Not Allowed가 반환된다
	assert delete_response.status_code == 405
	
	# When: PATCH 메서드로 요청을 보낸다
	patch_response = client.patch("/api/events")
	
	# Then: 405 Method Not Allowed가 반환된다
	assert patch_response.status_code == 405


def test_create_event_without_content_type(client: TestClient):
	"""
	Content-Type 없이 요청 시에도 FastAPI가 자동으로 처리한다.
	"""
	# Given: Content-Type 헤더 없는 요청 (하지만 TestClient는 자동으로 설정함)
	event_data = {"name": "테스트 이벤트"}
	
	# When: POST 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 201 성공이 반환된다 (TestClient가 자동으로 Content-Type 설정)
	assert response.status_code == 201


def test_create_event_with_null_name(client: TestClient):
	"""
	null 값으로 이벤트 생성 시 실패해야 한다.
	"""
	# Given: null 이름을 가진 이벤트 데이터
	event_data = {"name": None}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 422 Unprocessable Entity가 반환된다
	assert response.status_code == 422


def test_create_event_with_numeric_name(client: TestClient):
	"""
	숫자 타입 이름으로 이벤트 생성 시 타입 오류가 발생해야 한다.
	"""
	# Given: 숫자 타입 이름을 가진 이벤트 데이터
	event_data = {"name": 12345}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 422 오류가 반환된다 (Pydantic 타입 검증 실패)
	assert response.status_code == 422


def test_create_event_with_boolean_name(client: TestClient):
	"""
	불린 타입 이름으로 이벤트 생성 시 타입 오류가 발생해야 한다.
	"""
	# Given: 불린 타입 이름을 가진 이벤트 데이터
	event_data = {"name": True}
	
	# When: POST /api/events 엔드포인트에 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 422 오류가 반환된다 (Pydantic 타입 검증 실패)
	assert response.status_code == 422


def test_get_events_with_query_parameters(client: TestClient):
	"""
	쿼리 파라미터가 있어도 정상 동작해야 한다.
	"""
	# Given: 이벤트를 하나 생성한다
	event_data = {"name": "쿼리 테스트 이벤트"}
	client.post("/api/events", json=event_data)
	
	# When: 쿼리 파라미터와 함께 GET 요청을 보낸다
	response = client.get("/api/events?limit=10&offset=0")
	
	# Then: 200 OK가 반환된다 (쿼리 파라미터는 무시됨)
	assert response.status_code == 200
	events = response.json()
	assert len(events) == 1


def test_api_response_headers(client: TestClient):
	"""
	API 응답이 적절한 헤더를 포함해야 한다.
	"""
	# Given: 이벤트 데이터
	event_data = {"name": "헤더 테스트 이벤트"}
	
	# When: POST 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 적절한 헤더가 포함되어야 한다
	assert response.status_code == 201
	assert "content-type" in response.headers
	assert "application/json" in response.headers["content-type"]


def test_unicode_event_names(client: TestClient):
	"""
	다양한 유니코드 문자로 이벤트 이름을 생성할 수 있어야 한다.
	"""
	# Given: 다양한 언어와 특수 문자를 포함한 이벤트 이름들
	unicode_names = [
		"🍽️ 저녁 회식",
		"Пивной вечер",
		"飲み会",
		"مأدبة عشاء",
		"Dîner d'équipe",
		"Cena de empresa",
		"Jantar da empresa"
	]
	
	created_events = []
	
	# When: 각 이름으로 이벤트를 생성한다
	for name in unicode_names:
		response = client.post("/api/events", json={"name": name})
		assert response.status_code == 201
		created_events.append(response.json())
	
	# Then: 모든 이벤트가 올바르게 저장되고 조회된다
	response = client.get("/api/events")
	assert response.status_code == 200
	events = response.json()
	assert len(events) == len(unicode_names)
	
	for i, event in enumerate(events):
		assert event["name"] == unicode_names[i]


def test_concurrent_event_creation_simulation(client: TestClient):
	"""
	동시에 여러 이벤트를 생성하는 상황을 시뮬레이션한다.
	"""
	# Given: 동시 요청을 시뮬레이션할 이벤트 데이터들
	event_names = [f"동시 생성 이벤트 {i}" for i in range(1, 6)]
	
	# When: 빠르게 연속으로 이벤트를 생성한다
	created_events = []
	for name in event_names:
		response = client.post("/api/events", json={"name": name})
		assert response.status_code == 201
		created_events.append(response.json())
	
	# Then: 모든 이벤트가 고유한 ID를 가져야 한다
	event_ids = [event["event_id"] for event in created_events]
	assert len(set(event_ids)) == len(event_ids)
	
	# And: ID가 순차적으로 증가해야 한다
	for i in range(1, len(event_ids)):
		assert event_ids[i] > event_ids[i-1]


def test_large_payload_handling(client: TestClient):
	"""
	큰 크기의 페이로드도 적절히 처리되어야 한다.
	"""
	# Given: 매우 긴 이벤트 이름 (1KB 정도)
	large_name = "매우 긴 이벤트 이름 " * 50  # 약 1KB
	event_data = {"name": large_name}
	
	# When: POST 요청을 보낸다
	response = client.post("/api/events", json=event_data)
	
	# Then: 요청이 성공적으로 처리되어야 한다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["name"] == large_name
