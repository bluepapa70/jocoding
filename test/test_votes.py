"""
Tests for vote API endpoints.
"""
from fastapi.testclient import TestClient


def test_create_vote_success(client: TestClient):
	"""
	메뉴에 대한 투표를 성공적으로 생성해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 메뉴를 생성한다
	menu_data = {"name": "삼겹살"}
	menu_response = client.post(f"/api/events/{event_id}/menus", json=menu_data)
	assert menu_response.status_code == 201
	menu_id = menu_response.json()["id"]
	
	# And: 투표 데이터
	vote_data = {"menu_id": menu_id}
	
	# When: POST /api/events/{event_id}/votes 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{event_id}/votes", json=vote_data)
	
	# Then: 201 Created와 투표 정보가 반환된다
	assert response.status_code == 201
	response_data = response.json()
	assert response_data["vote_id"] == 1
	assert response_data["event_id"] == event_id
	assert response_data["menu_id"] == menu_id


def test_create_vote_event_not_found(client: TestClient):
	"""
	존재하지 않는 이벤트에 투표 시 404 오류가 반환되어야 한다.
	"""
	# Given: 존재하지 않는 이벤트 ID
	non_existent_event_id = 999
	vote_data = {"menu_id": 1}
	
	# When: POST /api/events/{event_id}/votes 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{non_existent_event_id}/votes", json=vote_data)
	
	# Then: 404 Not Found가 반환된다
	assert response.status_code == 404
	assert "Event not found" in response.json()["detail"]


def test_create_vote_menu_not_found(client: TestClient):
	"""
	존재하지 않는 메뉴에 투표 시 404 오류가 반환되어야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 존재하지 않는 메뉴 ID
	non_existent_menu_id = 999
	vote_data = {"menu_id": non_existent_menu_id}
	
	# When: POST /api/events/{event_id}/votes 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{event_id}/votes", json=vote_data)
	
	# Then: 404 Not Found가 반환된다
	assert response.status_code == 404
	assert "Menu not found" in response.json()["detail"]


def test_create_vote_menu_different_event(client: TestClient):
	"""
	다른 이벤트의 메뉴에 투표 시 400 오류가 반환되어야 한다.
	"""
	# Given: 첫 번째 이벤트와 메뉴를 생성한다
	event1_data = {"name": "2025년 7월 회식"}
	event1_response = client.post("/api/events", json=event1_data)
	assert event1_response.status_code == 201
	event1_id = event1_response.json()["event_id"]
	
	menu1_data = {"name": "삼겹살"}
	menu1_response = client.post(f"/api/events/{event1_id}/menus", json=menu1_data)
	assert menu1_response.status_code == 201
	menu1_id = menu1_response.json()["id"]
	
	# And: 두 번째 이벤트를 생성한다
	event2_data = {"name": "2025년 8월 회식"}
	event2_response = client.post("/api/events", json=event2_data)
	assert event2_response.status_code == 201
	event2_id = event2_response.json()["event_id"]
	
	# And: 첫 번째 이벤트의 메뉴에 두 번째 이벤트에서 투표하려는 데이터
	vote_data = {"menu_id": menu1_id}
	
	# When: POST /api/events/{event2_id}/votes 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{event2_id}/votes", json=vote_data)
	
	# Then: 400 Bad Request가 반환된다
	assert response.status_code == 400
	assert "Menu does not belong to this event" in response.json()["detail"]


def test_create_vote_invalid_data(client: TestClient):
	"""
	잘못된 데이터로 투표 생성 시 422 오류가 반환되어야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 잘못된 투표 데이터 (menu_id 필드 누락)
	invalid_vote_data = {}
	
	# When: POST /api/events/{event_id}/votes 엔드포인트에 요청을 보낸다
	response = client.post(f"/api/events/{event_id}/votes", json=invalid_vote_data)
	
	# Then: 422 Unprocessable Entity가 반환된다
	assert response.status_code == 422


def test_get_vote_results_no_votes(client: TestClient):
	"""
	투표가 없는 이벤트에서 메뉴 목록과 0 투표 수를 반환해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 메뉴를 생성한다
	menu_data = {"name": "삼겹살"}
	menu_response = client.post(f"/api/events/{event_id}/menus", json=menu_data)
	assert menu_response.status_code == 201
	menu_id = menu_response.json()["id"]
	
	# When: GET /api/events/{event_id}/results 엔드포인트에 요청을 보낸다
	response = client.get(f"/api/events/{event_id}/results")
	
	# Then: 200 OK와 메뉴별 투표 결과가 반환된다
	assert response.status_code == 200
	results = response.json()
	assert len(results) == 1
	assert results[0]["menu_id"] == menu_id
	assert results[0]["name"] == "삼겹살"
	assert results[0]["votes"] == 0


def test_get_vote_results_with_votes(client: TestClient):
	"""
	투표가 있는 이벤트에서 올바른 투표 결과를 반환해야 한다.
	"""
	# Given: 이벤트를 먼저 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# And: 여러 메뉴를 생성한다
	menu1_response = client.post(f"/api/events/{event_id}/menus", json={"name": "삼겹살"})
	assert menu1_response.status_code == 201
	menu1_id = menu1_response.json()["id"]
	
	menu2_response = client.post(f"/api/events/{event_id}/menus", json={"name": "치킨"})
	assert menu2_response.status_code == 201
	menu2_id = menu2_response.json()["id"]
	
	# And: 투표를 생성한다 (삼겹살에 3표, 치킨에 2표)
	for _ in range(3):
		vote_response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu1_id})
		assert vote_response.status_code == 201
	
	for _ in range(2):
		vote_response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu2_id})
		assert vote_response.status_code == 201
	
	# When: GET /api/events/{event_id}/results 엔드포인트에 요청을 보낸다
	response = client.get(f"/api/events/{event_id}/results")
	
	# Then: 200 OK와 올바른 투표 결과가 반환된다
	assert response.status_code == 200
	results = response.json()
	assert len(results) == 2
	
	# 결과를 menu_id별로 정리
	results_by_menu = {result["menu_id"]: result for result in results}
	
	assert results_by_menu[menu1_id]["name"] == "삼겹살"
	assert results_by_menu[menu1_id]["votes"] == 3
	
	assert results_by_menu[menu2_id]["name"] == "치킨"
	assert results_by_menu[menu2_id]["votes"] == 2


def test_get_vote_results_event_not_found(client: TestClient):
	"""
	존재하지 않는 이벤트의 투표 결과 조회 시 404 오류가 반환되어야 한다.
	"""
	# Given: 존재하지 않는 이벤트 ID
	non_existent_event_id = 999
	
	# When: GET /api/events/{event_id}/results 엔드포인트에 요청을 보낸다
	response = client.get(f"/api/events/{non_existent_event_id}/results")
	
	# Then: 404 Not Found가 반환된다
	assert response.status_code == 404
	assert "Event not found" in response.json()["detail"]


def test_multiple_votes_same_menu(client: TestClient):
	"""
	같은 메뉴에 여러 번 투표할 수 있어야 한다.
	"""
	# Given: 이벤트와 메뉴를 생성한다
	event_data = {"name": "2025년 7월 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	menu_data = {"name": "삼겹살"}
	menu_response = client.post(f"/api/events/{event_id}/menus", json=menu_data)
	assert menu_response.status_code == 201
	menu_id = menu_response.json()["id"]
	
	# When: 같은 메뉴에 여러 번 투표한다
	vote_count = 5
	created_votes = []
	
	for i in range(vote_count):
		vote_response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu_id})
		assert vote_response.status_code == 201
		created_votes.append(vote_response.json())
	
	# Then: 각 투표가 고유한 ID를 가져야 한다
	vote_ids = [vote["vote_id"] for vote in created_votes]
	assert len(set(vote_ids)) == len(vote_ids)  # 모든 ID가 고유해야 함
	
	# And: 투표 결과에 올바른 투표 수가 반영되어야 한다
	results_response = client.get(f"/api/events/{event_id}/results")
	assert results_response.status_code == 200
	results = results_response.json()
	assert len(results) == 1
	assert results[0]["votes"] == vote_count
