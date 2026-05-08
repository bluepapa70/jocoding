"""
End-to-End test scenarios for Event API.
실제 사용자 흐름을 시뮬레이션하는 통합 테스트입니다.
"""
from fastapi.testclient import TestClient


def test_scenario_1_single_user_event_workflow(client: TestClient):
	"""
	시나리오 1: 단일 사용자가 이벤트를 생성하고 조회하는 전체 워크플로우
	
	사용자 스토리:
	- 사용자가 새로운 회식 이벤트를 생성한다
	- 생성된 이벤트 정보를 확인한다
	- 전체 이벤트 목록을 조회하여 자신의 이벤트가 포함되어 있는지 확인한다
	"""
	print("\n🔄 시나리오 1: 단일 사용자 이벤트 워크플로우 시작")
	
	# Step 1: 초기 상태 확인 - 이벤트가 없어야 함
	print("📋 Step 1: 초기 이벤트 목록 확인")
	response = client.get("/api/events")
	assert response.status_code == 200
	initial_events = response.json()
	initial_count = len(initial_events)
	print(f"   초기 이벤트 수: {initial_count}")
	
	# Step 2: 새로운 이벤트 생성
	print("🎉 Step 2: 새로운 회식 이벤트 생성")
	event_data = {
		"name": "2025년 7월 팀 빌딩 회식"
	}
	response = client.post("/api/events", json=event_data)
	assert response.status_code == 201
	created_event = response.json()
	
	print(f"   생성된 이벤트 ID: {created_event['event_id']}")
	print(f"   생성된 이벤트 이름: {created_event['name']}")
	
	# 생성된 이벤트 검증
	assert "event_id" in created_event
	assert "name" in created_event
	assert created_event["name"] == event_data["name"]
	assert isinstance(created_event["event_id"], int)
	assert created_event["event_id"] > 0
	
	# Step 3: 이벤트 목록 조회하여 생성된 이벤트 확인
	print("📝 Step 3: 이벤트 목록에서 생성된 이벤트 확인")
	response = client.get("/api/events")
	assert response.status_code == 200
	all_events = response.json()
	
	print(f"   전체 이벤트 수: {len(all_events)}")
	assert len(all_events) == initial_count + 1
	
	# 생성된 이벤트가 목록에 포함되어 있는지 확인
	created_event_found = False
	for event in all_events:
		if event["event_id"] == created_event["event_id"]:
			created_event_found = True
			assert event["name"] == created_event["name"]
			print(f"   ✅ 생성된 이벤트 발견: {event['name']}")
			break
	
	assert created_event_found, "생성된 이벤트가 목록에서 찾을 수 없습니다"
	
	print("✅ 시나리오 1 완료: 단일 사용자 워크플로우 성공")


def test_scenario_2_multiple_events_management(client: TestClient):
	"""
	시나리오 2: 여러 이벤트를 생성하고 관리하는 시나리오
	
	사용자 스토리:
	- 관리자가 여러 회식 이벤트를 계획한다
	- 각기 다른 목적의 이벤트들을 순차적으로 생성한다
	- 모든 이벤트가 올바르게 저장되고 조회되는지 확인한다
	- 이벤트 ID가 순차적으로 할당되는지 확인한다
	"""
	print("\n🔄 시나리오 2: 다중 이벤트 관리 시나리오 시작")
	
	# Step 1: 초기 상태 확인
	print("📋 Step 1: 초기 상태 확인")
	response = client.get("/api/events")
	assert response.status_code == 200
	initial_events = response.json()
	initial_count = len(initial_events)
	print(f"   초기 이벤트 수: {initial_count}")
	
	# Step 2: 여러 이벤트 생성 계획
	print("📅 Step 2: 여러 이벤트 생성 계획")
	planned_events = [
		{"name": "신입사원 환영 회식", "purpose": "신입사원 환영"},
		{"name": "프로젝트 완료 축하 파티", "purpose": "프로젝트 성공 축하"},
		{"name": "분기별 팀 빌딩", "purpose": "팀워크 강화"},
		{"name": "연말 송년회", "purpose": "한 해 마무리"},
		{"name": "부서간 친목 도모", "purpose": "부서간 협력 증진"}
	]
	
	print(f"   계획된 이벤트 수: {len(planned_events)}")
	
	# Step 3: 이벤트들을 순차적으로 생성
	print("🎉 Step 3: 이벤트들 순차 생성")
	created_events = []
	
	for i, event_plan in enumerate(planned_events):
		print(f"   생성 중 ({i+1}/{len(planned_events)}): {event_plan['name']}")
		
		response = client.post("/api/events", json={"name": event_plan["name"]})
		assert response.status_code == 201
		
		created_event = response.json()
		created_events.append(created_event)
		
		# 각 이벤트 생성 검증
		assert created_event["name"] == event_plan["name"]
		assert isinstance(created_event["event_id"], int)
		print(f"      ✅ 생성 완료 - ID: {created_event['event_id']}")
	
	# Step 4: ID 순차성 검증
	print("🔢 Step 4: 이벤트 ID 순차성 검증")
	event_ids = [event["event_id"] for event in created_events]
	
	for i in range(1, len(event_ids)):
		assert event_ids[i] > event_ids[i-1], f"ID가 순차적이지 않음: {event_ids[i-1]} -> {event_ids[i]}"
	
	print(f"   ✅ ID 순차성 확인: {event_ids}")
	
	# Step 5: 전체 목록 조회 및 검증
	print("📝 Step 5: 전체 이벤트 목록 검증")
	response = client.get("/api/events")
	assert response.status_code == 200
	all_events = response.json()
	
	expected_total = initial_count + len(planned_events)
	assert len(all_events) == expected_total
	print(f"   전체 이벤트 수: {len(all_events)} (예상: {expected_total})")
	
	# 모든 생성된 이벤트가 목록에 포함되어 있는지 확인
	for created_event in created_events:
		found = False
		for event in all_events:
			if event["event_id"] == created_event["event_id"]:
				assert event["name"] == created_event["name"]
				found = True
				break
		assert found, f"이벤트 ID {created_event['event_id']}가 목록에서 누락됨"
	
	print("✅ 시나리오 2 완료: 다중 이벤트 관리 성공")


def test_scenario_3_real_world_usage_simulation(client: TestClient):
	"""
	시나리오 3: 실제 회사에서의 사용 패턴을 시뮬레이션
	
	사용자 스토리:
	- 여러 부서에서 동시에 회식 이벤트를 계획한다
	- 다양한 형태의 이벤트 이름들이 사용된다 (특수문자, 이모지 포함)
	- 중간중간 이벤트 목록을 조회하여 현재 상황을 파악한다
	- 잘못된 요청도 포함하여 실제 사용 환경을 시뮬레이션한다
	"""
	print("\n🔄 시나리오 3: 실제 사용 패턴 시뮬레이션 시작")
	
	# Step 1: 초기 상태 확인
	print("📋 Step 1: 초기 상태 확인")
	response = client.get("/api/events")
	assert response.status_code == 200
	initial_count = len(response.json())
	print(f"   초기 이벤트 수: {initial_count}")
	
	# Step 2: 영업팀 이벤트 생성
	print("💼 Step 2: 영업팀 이벤트 생성")
	sales_events = [
		"🎯 Q3 목표 달성 축하 회식",
		"영업팀 워크샵 & 네트워킹",
		"신규 고객사 계약 성공 파티"
	]
	
	sales_created = []
	for event_name in sales_events:
		response = client.post("/api/events", json={"name": event_name})
		assert response.status_code == 201
		sales_created.append(response.json())
		print(f"   ✅ 생성: {event_name}")
	
	# Step 3: 중간 상태 조회
	print("📊 Step 3: 중간 상태 조회")
	response = client.get("/api/events")
	assert response.status_code == 200
	current_events = response.json()
	print(f"   현재 이벤트 수: {len(current_events)}")
	
	# Step 4: 개발팀 이벤트 생성 (일부 실패 포함)
	print("💻 Step 4: 개발팀 이벤트 생성 (오류 처리 포함)")
	
	# 정상적인 개발팀 이벤트들
	dev_events = [
		"🚀 신규 서비스 런칭 기념 회식",
		"개발팀 코드 리뷰 & 맛집 탐방",
		"Tech Talk & Beer Night"
	]
	
	dev_created = []
	for event_name in dev_events:
		response = client.post("/api/events", json={"name": event_name})
		assert response.status_code == 201
		dev_created.append(response.json())
		print(f"   ✅ 생성: {event_name}")
	
	# 잘못된 요청 시뮬레이션
	print("   ❌ 잘못된 요청들 테스트:")
	
	# 필수 필드 누락
	response = client.post("/api/events", json={})
	assert response.status_code == 422
	print("      ✅ 필수 필드 누락 오류 처리 확인")
	
	# 잘못된 타입
	response = client.post("/api/events", json={"name": 12345})
	assert response.status_code == 422
	print("      ✅ 잘못된 타입 오류 처리 확인")
	
	# Step 5: HR팀 특수 이벤트 생성
	print("👥 Step 5: HR팀 다국어 & 특수문자 이벤트 생성")
	hr_events = [
		"新入社員歓迎会 (신입사원 환영회)",
		"Diversity & Inclusion Dinner 🌍",
		"직원 만족도 조사 결과 공유회",
		"Work-Life Balance 세미나 & 식사"
	]
	
	hr_created = []
	for event_name in hr_events:
		response = client.post("/api/events", json={"name": event_name})
		assert response.status_code == 201
		hr_created.append(response.json())
		print(f"   ✅ 생성: {event_name}")
	
	# Step 6: 최종 상태 검증
	print("🎯 Step 6: 최종 상태 종합 검증")
	response = client.get("/api/events")
	assert response.status_code == 200
	final_events = response.json()
	
	# 총 생성된 이벤트 수 계산
	total_created = len(sales_events) + len(dev_events) + len(hr_events)
	expected_total = initial_count + total_created
	
	assert len(final_events) == expected_total
	print(f"   최종 이벤트 수: {len(final_events)} (예상: {expected_total})")
	
	# Step 7: 데이터 무결성 검증
	print("🔍 Step 7: 데이터 무결성 최종 검증")
	
	# 모든 생성된 이벤트들이 목록에 포함되어 있는지 확인
	all_created = sales_created + dev_created + hr_created
	
	for created_event in all_created:
		found = False
		for event in final_events:
			if event["event_id"] == created_event["event_id"]:
				assert event["name"] == created_event["name"]
				found = True
				break
		assert found, f"이벤트가 누락됨: {created_event}"
	
	print("   ✅ 모든 생성된 이벤트 확인 완료")
	
	# ID 중복 검증
	event_ids = [event["event_id"] for event in final_events]
	unique_ids = set(event_ids)
	assert len(event_ids) == len(unique_ids), "중복된 이벤트 ID 발견"
	print("   ✅ 이벤트 ID 중복 없음 확인")
	
	# 이벤트 이름 다양성 검증
	event_names = [event["name"] for event in final_events]
	print(f"   📝 다양한 이벤트 이름 확인:")
	for name in event_names[-5:]:  # 마지막 5개만 출력
		print(f"      - {name}")
	
	print("✅ 시나리오 3 완료: 실제 사용 패턴 시뮬레이션 성공")


def test_end_to_end_comprehensive_workflow(client: TestClient):
	"""
	통합 E2E 테스트: 전체 시스템의 종합적인 동작 검증
	
	이 테스트는 위의 3개 시나리오를 모두 포함하여
	실제 운영 환경에서의 전체적인 워크플로우를 검증합니다.
	"""
	print("\n🔄 통합 E2E 테스트 시작")
	print("=" * 60)
	
	# 초기 상태 기록
	response = client.get("/api/events")
	initial_state = response.json()
	print(f"🏁 테스트 시작 시점 이벤트 수: {len(initial_state)}")
	
	# 시나리오들 실행
	scenario_results = []
	
	try:
		# 각 시나리오 실행 전후 상태 추적
		print("\n" + "="*60)
		print("시나리오 1 실행")
		before_s1 = len(client.get("/api/events").json())
		test_scenario_1_single_user_event_workflow(client)
		after_s1 = len(client.get("/api/events").json())
		scenario_results.append(("시나리오 1", before_s1, after_s1, after_s1 - before_s1))
		
		print("\n" + "="*60)
		print("시나리오 2 실행")
		before_s2 = len(client.get("/api/events").json())
		test_scenario_2_multiple_events_management(client)
		after_s2 = len(client.get("/api/events").json())
		scenario_results.append(("시나리오 2", before_s2, after_s2, after_s2 - before_s2))
		
		print("\n" + "="*60)
		print("시나리오 3 실행")
		before_s3 = len(client.get("/api/events").json())
		test_scenario_3_real_world_usage_simulation(client)
		after_s3 = len(client.get("/api/events").json())
		scenario_results.append(("시나리오 3", before_s3, after_s3, after_s3 - before_s3))
		
	except Exception as e:
		print(f"❌ 시나리오 실행 중 오류 발생: {e}")
		raise
	
	# 최종 결과 요약
	print("\n" + "="*60)
	print("🎯 통합 E2E 테스트 결과 요약")
	print("="*60)
	
	for scenario_name, before, after, created in scenario_results:
		print(f"{scenario_name}:")
		print(f"  시작: {before}개 → 종료: {after}개 (생성: +{created}개)")
	
	final_count = len(client.get("/api/events").json())
	total_created = sum(result[3] for result in scenario_results)
	
	print(f"\n📊 최종 통계:")
	print(f"  초기 이벤트 수: {len(initial_state)}")
	print(f"  총 생성된 이벤트: {total_created}")
	print(f"  최종 이벤트 수: {final_count}")
	print(f"  예상 vs 실제: {len(initial_state) + total_created} vs {final_count}")
	
	# 최종 검증
	assert final_count == len(initial_state) + total_created
	print("✅ 통합 E2E 테스트 완료: 모든 시나리오 성공")
	print("="*60)
