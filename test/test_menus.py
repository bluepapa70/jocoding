"""
Tests for menu API endpoints.
"""
from fastapi.testclient import TestClient


def test_create_menu_success(client: TestClient):
	"""
	이벤트에 새로운 메뉴 후보를 성공적으로 생성해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 메뉴 생성 데이터
	menu_data = {"name": "삼겹살"}
	
	# When: POST /api/events/{event_id}/menus 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{event_id}/menus", json=menu_data)
	
	# Then: 201 Created와 메뉴 정보가 반환된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["id"] == 1
	assert response_data["event_id"] == event_id
	assert response_data["name"] == "삼겹살"


def test_create_menu_event_not_found(client: TestClient):
	"""
	존재하지 않는 이벤트에 메뉴 생성 시 404 오류가 반환되어야 한다.
	"""
	# Given: 존재하지 않는 이벤트 ID
	non_existent_event_id = 999
	menu_data = {"name": "치킨"}
	
	# When: POST /api/events/{event_id}/menus 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{non_existent_event_id}/menus", json=menu_data)
	
	# Then: 404 Not Found가 반환된다
	assert response.status_code == 404
	assert "Event not found" in response.json()["detail"]


def test_create_menu_invalid_data(client: TestClient):
	"""
	잘못된 데이터로 메뉴 생성 시 422 오류가 반환되어야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 잘못된 메뉴 데이터 (name 필드 누락)
	invalid_menu_data = {}
	
	# When: POST /api/events/{event_id}/menus 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{event_id}/menus", json=invalid_menu_data)
	
	# Then: 422 Unprocessable Entity가 반환된다
	assert response.status_code == 422


def test_get_menus_empty(client: TestClient):
	"""
	메뉴가 없는 이벤트에서 빈 리스트를 반환해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# When: GET /api/events/{event_id}/menus 엔드포인트에 요청을 보낸다
	response = client.get(f"/api/events/{event_id}/menus")
	
	# Then: 200 OK와 빈 리스트가 반환된다
	assert response.status_code == 200
	assert response.json() == []


def test_get_menus_with_data(client: TestClient):
	"""
	메뉴가 있는 이벤트에서 메뉴 목록을 반환해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 여러 메뉴를 생성한다
	menu_names = ["삼겹살", "치킨", "피자"]
	for menu_name in menu_names:
		menu_response = client.post(f"/api/events/{event_id}/menus", json={"name": menu_name})
		assert menu_response.status_code == 201
	
	# When: GET /api/events/{event_id}/menus 엔드포인트에 요청을 보낸다
	response = client.get(f"/api/events/{event_id}/menus")
	
	# Then: 200 OK와 메뉴 목록이 반환된다
	assert response.status_code == 200
	menus = response.json()
	assert len(menus) == 3
	
	returned_names = [menu["name"] for menu in menus]
	for name in menu_names:
		assert name in returned_names


def test_get_menus_event_not_found(client: TestClient):
	"""
	존재하지 않는 이벤트의 메뉴 조회 시 404 오류가 반환되어야 한다.
	"""
	# Given: 존재하지 않는 이벤트 ID
	non_existent_event_id = 999
	
	# When: GET /api/events/{event_id}/menus 엔드포인트에 요청을 보낸다
	response = client.get(f"/api/events/{non_existent_event_id}/menus")
	
	# Then: 404 Not Found가 반환된다
	assert response.status_code == 404
	assert "Event not found" in response.json()["detail"]


def test_create_multiple_menus_same_event(client: TestClient):
	"""
	같은 이벤트에 여러 메뉴를 생성할 수 있어야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# When: 여러 메뉴를 생성한다
	menu_names = ["한식", "중식", "일식", "양식", "분식"]
	created_menus = []
	
	for menu_name in menu_names:
		response = client.post(f"/api/events/{event_id}/menus", json={"name": menu_name})
		assert response.status_code == 201
		created_menus.append(response.json())
	
	# Then: 각 메뉴가 고유한 ID를 가져야 한다
	menu_ids = [menu["id"] for menu in created_menus]
	assert len(set(menu_ids)) == len(menu_ids)  # 모든 ID가 고유해야 함
	
	# And: 모든 메뉴가 같은 이벤트에 속해야 한다
	for menu in created_menus:
		assert menu["event_id"] == event_id


def test_menu_id_sequence(client: TestClient):
	"""
	메뉴 ID가 순차적으로 증가해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# When: 여러 메뉴를 순차적으로 생성한다
	menu_names = ["첫 번째 메뉴", "두 번째 메뉴", "세 번째 메뉴"]
	created_ids = []
	
	for menu_name in menu_names:
		response = client.post(f"/api/events/{event_id}/menus", json={"name": menu_name})
		assert response.status_code == 201
		created_ids.append(response.json()["id"])
	
	# Then: ID가 순차적으로 증가해야 한다
	for i in range(1, len(created_ids)):
		assert created_ids[i] > created_ids[i-1]
