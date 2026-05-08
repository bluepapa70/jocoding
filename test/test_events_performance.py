"""
Performance and stress tests for Event API endpoints.
"""
import time
from fastapi.testclient import TestClient


def test_api_response_time_create_event(client: TestClient):
	"""
	이벤트 생성 API의 응답 시간이 합리적이어야 한다.
	"""
	# Given: 이벤트 데이터
	event_data = {"name": "성능 테스트 이벤트"}
	
	# When: 응답 시간을 측정하며 요청을 보낸다
	start_time = time.time()
	response = client.post("/api/events", json=event_data)
	end_time = time.time()
	
	# Then: 요청이 성공하고 응답 시간이 1초 미만이어야 한다
	assert response.status_code == 201
	response_time = end_time - start_time
	assert response_time < 1.0, f"Response time too slow: {response_time:.3f}s"


def test_api_response_time_get_events(client: TestClient):
	"""
	이벤트 목록 조회 API의 응답 시간이 합리적이어야 한다.
	"""
	# Given: 여러 이벤트를 미리 생성한다
	for i in range(10):
		client.post("/api/events", json={"name": f"이벤트 {i}"})
	
	# When: 응답 시간을 측정하며 목록을 조회한다
	start_time = time.time()
	response = client.get("/api/events")
	end_time = time.time()
	
	# Then: 요청이 성공하고 응답 시간이 1초 미만이어야 한다
	assert response.status_code == 200
	response_time = end_time - start_time
	assert response_time < 1.0, f"Response time too slow: {response_time:.3f}s"


def test_create_many_events_performance(client: TestClient):
	"""
	많은 이벤트를 순차적으로 생성할 때의 성능을 테스트한다.
	"""
	# Given: 100개의 이벤트를 생성할 데이터
	num_events = 100
	
	# When: 100개의 이벤트를 순차적으로 생성한다
	start_time = time.time()
	
	for i in range(num_events):
		response = client.post("/api/events", json={"name": f"대량 생성 이벤트 {i}"})
		assert response.status_code == 201
	
	end_time = time.time()
	
	# Then: 전체 작업이 10초 미만에 완료되어야 한다
	total_time = end_time - start_time
	assert total_time < 10.0, f"Mass creation too slow: {total_time:.3f}s"
	
	# And: 평균 응답 시간이 100ms 미만이어야 한다
	average_time = total_time / num_events
	assert average_time < 0.1, f"Average response time too slow: {average_time:.3f}s"


def test_get_large_event_list_performance(client: TestClient):
	"""
	큰 이벤트 목록을 조회할 때의 성능을 테스트한다.
	"""
	# Given: 100개의 이벤트를 미리 생성한다
	num_events = 100
	for i in range(num_events):
		response = client.post("/api/events", json={"name": f"대량 조회 테스트 이벤트 {i}"})
		assert response.status_code == 201
	
	# When: 대량의 이벤트 목록을 조회한다
	start_time = time.time()
	response = client.get("/api/events")
	end_time = time.time()
	
	# Then: 요청이 성공하고 응답 시간이 2초 미만이어야 한다
	assert response.status_code == 200
	response_time = end_time - start_time
	assert response_time < 2.0, f"Large list retrieval too slow: {response_time:.3f}s"
	
	# And: 올바른 수의 이벤트가 반환되어야 한다
	events = response.json()
	assert len(events) == num_events


def test_memory_usage_with_large_event_names(client: TestClient):
	"""
	큰 이벤트 이름들을 처리할 때 메모리 사용량을 테스트한다.
	"""
	# Given: 큰 크기의 이벤트 이름들
	large_name_base = "매우 긴 이벤트 이름을 가진 테스트 " * 50  # 약 1.5KB
	
	# When: 10개의 큰 이벤트를 생성한다
	for i in range(10):
		large_name = f"{large_name_base} {i}"
		response = client.post("/api/events", json={"name": large_name})
		assert response.status_code == 201
	
	# Then: 목록 조회가 정상적으로 작동해야 한다
	response = client.get("/api/events")
	assert response.status_code == 200
	events = response.json()
	assert len(events) == 10
	
	# And: 모든 이벤트의 이름이 올바르게 저장되어야 한다
	for i, event in enumerate(events):
		expected_name = f"{large_name_base} {i}"
		assert event["name"] == expected_name


def test_concurrent_request_simulation(client: TestClient):
	"""
	동시 요청을 시뮬레이션하여 데이터 일관성을 테스트한다.
	"""
	# Given: 동시 요청을 시뮬레이션할 이벤트 이름들
	event_names = [f"동시 요청 테스트 {i}" for i in range(20)]
	
	# When: 빠르게 연속으로 이벤트를 생성한다 (동시성 시뮬레이션)
	created_events = []
	for name in event_names:
		response = client.post("/api/events", json={"name": name})
		assert response.status_code == 201
		created_events.append(response.json())
	
	# Then: 모든 이벤트가 고유한 ID를 가져야 한다
	event_ids = [event["event_id"] for event in created_events]
	assert len(set(event_ids)) == len(event_ids), "Duplicate IDs found"
	
	# And: ID가 연속적이어야 한다
	sorted_ids = sorted(event_ids)
	for i in range(1, len(sorted_ids)):
		assert sorted_ids[i] == sorted_ids[i-1] + 1, "Non-sequential IDs found"


def test_api_stability_under_load(client: TestClient):
	"""
	반복적인 요청 하에서 API의 안정성을 테스트한다.
	"""
	# Given: 반복 테스트를 위한 설정
	iterations = 50
	
	# When: 생성과 조회를 반복한다
	for i in range(iterations):
		# 이벤트 생성
		create_response = client.post("/api/events", json={"name": f"안정성 테스트 {i}"})
		assert create_response.status_code == 201
		
		# 목록 조회
		get_response = client.get("/api/events")
		assert get_response.status_code == 200
		events = get_response.json()
		assert len(events) == i + 1
	
	# Then: 최종 상태가 일관되어야 한다
	final_response = client.get("/api/events")
	assert final_response.status_code == 200
	final_events = final_response.json()
	assert len(final_events) == iterations
