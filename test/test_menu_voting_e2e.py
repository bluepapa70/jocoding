"""
End-to-End test scenarios for Menu Voting System.
전체 메뉴 투표 시스템의 E2E 테스트입니다.
"""
from fastapi.testclient import TestClient


def test_complete_menu_voting_workflow(client: TestClient):
	"""
	완전한 메뉴 투표 워크플로우 E2E 테스트
	
	사용자 스토리:
	1. 관리자가 회식 이벤트를 생성한다
	2. 참여자들이 다양한 메뉴 후보를 제안한다
	3. 참여자들이 선호하는 메뉴에 투표한다
	4. 투표 결과를 확인하고 최종 메뉴를 선정한다
	"""
	print("\n🔄 완전한 메뉴 투표 워크플로우 E2E 테스트 시작")
	print("=" * 60)
	
	# Step 1: 이벤트 생성
	print("📅 Step 1: 회식 이벤트 생성")
	event_data = {"name": "2025년 팀 빌딩 회식"}
	event_response = client.post("/api/events", json=event_data)
	assert event_response.status_code == 201
	
	event = event_response.json()
	event_id = event["event_id"]
	print(f"   ✅ 이벤트 생성 완료: '{event['name']}' (ID: {event_id})")
	
	# Step 2: 메뉴 후보 제안
	print(f"\n🍽️ Step 2: 메뉴 후보 제안 (이벤트 ID: {event_id})")
	menu_candidates = [
		"삼겹살 구이",
		"치킨 & 맥주", 
		"피자 파티",
		"회 & 초밥",
		"중식 코스",
		"이탈리안 레스토랑",
		"한정식"
	]
	
	created_menus = []
	for menu_name in menu_candidates:
		menu_response = client.post(f"/api/events/{event_id}/menus", json={"name": menu_name})
		assert menu_response.status_code == 201
		menu = menu_response.json()
		created_menus.append(menu)
		print(f"   ✅ 메뉴 후보 추가: '{menu_name}' (ID: {menu['id']})")
	
	# 메뉴 목록 확인
	menus_response = client.get(f"/api/events/{event_id}/menus")
	assert menus_response.status_code == 200
	all_menus = menus_response.json()
	assert len(all_menus) == len(menu_candidates)
	print(f"   📋 총 {len(all_menus)}개 메뉴 후보 등록 완료")
	
	# Step 3: 투표 진행
	print(f"\n🗳️ Step 3: 투표 진행")
	# 실제적인 투표 분포 시뮬레이션
	vote_distribution = {
		created_menus[0]["id"]: 12,  # 삼겹살 구이: 12표
		created_menus[1]["id"]: 18,  # 치킨 & 맥주: 18표 (1위)
		created_menus[2]["id"]: 8,   # 피자 파티: 8표
		created_menus[3]["id"]: 15,  # 회 & 초밥: 15표 (2위)
		created_menus[4]["id"]: 5,   # 중식 코스: 5표
		created_menus[5]["id"]: 10,  # 이탈리안: 10표
		created_menus[6]["id"]: 14   # 한정식: 14표 (3위)
	}
	
	total_votes = 0
	for menu_id, vote_count in vote_distribution.items():
		for _ in range(vote_count):
			vote_response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu_id})
			assert vote_response.status_code == 201
		total_votes += vote_count
		
		# 해당 메뉴 이름 찾기
		menu_name = next(menu["name"] for menu in created_menus if menu["id"] == menu_id)
		print(f"   ✅ '{menu_name}'에 {vote_count}표 투표 완료")
	
	print(f"   📊 총 투표 수: {total_votes}표")
	
	# Step 4: 투표 결과 조회 및 검증
	print(f"\n📈 Step 4: 투표 결과 조회 및 분석")
	results_response = client.get(f"/api/events/{event_id}/results")
	assert results_response.status_code == 200
	
	results = results_response.json()
	assert len(results) == len(menu_candidates)
	
	# 결과를 투표 수 기준으로 정렬
	sorted_results = sorted(results, key=lambda x: x["votes"], reverse=True)
	
	print("   🏆 투표 결과 (득표수 순):")
	for i, result in enumerate(sorted_results, 1):
		percentage = (result["votes"] / total_votes) * 100
		print(f"      {i}위: {result['name']} - {result['votes']}표 ({percentage:.1f}%)")
	
	# 결과 검증
	winner = sorted_results[0]
	runner_up = sorted_results[1]
	third_place = sorted_results[2]
	
	assert winner["name"] == "치킨 & 맥주"
	assert winner["votes"] == 18
	assert runner_up["name"] == "회 & 초밥"
	assert runner_up["votes"] == 15
	assert third_place["name"] == "한정식"
	assert third_place["votes"] == 14
	
	print(f"\n🎯 Step 5: 최종 결과")
	print(f"   🥇 최종 선정 메뉴: {winner['name']} ({winner['votes']}표)")
	print(f"   🥈 2위: {runner_up['name']} ({runner_up['votes']}표)")
	print(f"   🥉 3위: {third_place['name']} ({third_place['votes']}표)")
	
	# 투표 결과 합계 검증
	total_result_votes = sum(result["votes"] for result in results)
	assert total_result_votes == total_votes
	print(f"   ✅ 투표 집계 검증 완료: {total_result_votes}표")
	
	print("\n✅ 완전한 메뉴 투표 워크플로우 E2E 테스트 성공!")
	print("=" * 60)


def test_multiple_events_independent_voting(client: TestClient):
	"""
	여러 이벤트의 독립적인 투표 시스템 테스트
	
	사용자 스토리:
	- 여러 부서에서 각각 독립적인 회식 이벤트를 진행한다
	- 각 이벤트의 메뉴와 투표는 서로 영향을 주지 않는다
	"""
	print("\n🔄 다중 이벤트 독립 투표 시스템 테스트 시작")
	print("=" * 60)
	
	# 두 개의 독립적인 이벤트 생성
	events_data = [
		{"name": "개발팀 회식", "menus": ["삼겹살", "치킨", "피자"]},
		{"name": "영업팀 회식", "menus": ["한우", "랍스터", "와인"]}
	]
	
	event_results = []
	
	for event_data in events_data:
		print(f"\n📅 이벤트 생성: {event_data['name']}")
		
		# 이벤트 생성
		event_response = client.post("/api/events", json={"name": event_data["name"]})
		assert event_response.status_code == 201
		event = event_response.json()
		event_id = event["event_id"]
		
		# 메뉴 추가
		menu_ids = []
		for menu_name in event_data["menus"]:
			menu_response = client.post(f"/api/events/{event_id}/menus", json={"name": menu_name})
			assert menu_response.status_code == 201
			menu_ids.append(menu_response.json()["id"])
			print(f"   ✅ 메뉴 추가: {menu_name}")
		
		# 투표 (각 메뉴에 다른 수의 투표)
		votes_per_menu = [5, 8, 3]  # 첫 번째 메뉴 5표, 두 번째 8표, 세 번째 3표
		for menu_id, vote_count in zip(menu_ids, votes_per_menu):
			for _ in range(vote_count):
				vote_response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu_id})
				assert vote_response.status_code == 201
		
		# 결과 확인
		results_response = client.get(f"/api/events/{event_id}/results")
		assert results_response.status_code == 200
		results = results_response.json()
		
		event_results.append({
			"event_id": event_id,
			"name": event_data["name"],
			"results": results
		})
		
		print(f"   📊 {event_data['name']} 투표 결과:")
		for result in sorted(results, key=lambda x: x["votes"], reverse=True):
			print(f"      {result['name']}: {result['votes']}표")
	
	# 독립성 검증
	print(f"\n🔍 이벤트 독립성 검증:")
	
	# 첫 번째 이벤트 검증
	dev_results = event_results[0]["results"]
	dev_winner = max(dev_results, key=lambda x: x["votes"])
	assert dev_winner["name"] == "치킨"
	assert dev_winner["votes"] == 8
	print(f"   ✅ 개발팀 1위: {dev_winner['name']} ({dev_winner['votes']}표)")
	
	# 두 번째 이벤트 검증
	sales_results = event_results[1]["results"]
	sales_winner = max(sales_results, key=lambda x: x["votes"])
	assert sales_winner["name"] == "랍스터"
	assert sales_winner["votes"] == 8
	print(f"   ✅ 영업팀 1위: {sales_winner['name']} ({sales_winner['votes']}표)")
	
	# 메뉴 ID 중복 없음 확인
	all_menu_ids = []
	for event_result in event_results:
		for result in event_result["results"]:
			all_menu_ids.append(result["menu_id"])
	
	assert len(set(all_menu_ids)) == len(all_menu_ids), "메뉴 ID 중복 발견"
	print(f"   ✅ 메뉴 ID 독립성 확인 완료")
	
	print("\n✅ 다중 이벤트 독립 투표 시스템 테스트 성공!")
	print("=" * 60)


def test_error_handling_comprehensive(client: TestClient):
	"""
	포괄적인 오류 처리 테스트
	"""
	print("\n🔄 포괄적인 오류 처리 테스트 시작")
	print("=" * 60)
	
	# 1. 존재하지 않는 이벤트에 메뉴 추가 시도
	print("❌ Test 1: 존재하지 않는 이벤트에 메뉴 추가")
	response = client.post("/api/events/999/menus", json={"name": "테스트 메뉴"})
	assert response.status_code == 404
	print("   ✅ 404 오류 정상 반환")
	
	# 2. 존재하지 않는 이벤트에 투표 시도
	print("❌ Test 2: 존재하지 않는 이벤트에 투표")
	response = client.post("/api/events/999/votes", json={"menu_id": 1})
	assert response.status_code == 404
	print("   ✅ 404 오류 정상 반환")
	
	# 3. 존재하지 않는 메뉴에 투표 시도
	print("❌ Test 3: 존재하지 않는 메뉴에 투표")
	# 먼저 이벤트 생성
	event_response = client.post("/api/events", json={"name": "테스트 이벤트"})
	assert event_response.status_code == 201
	event_id = event_response.json()["event_id"]
	
	# 존재하지 않는 메뉴에 투표
	response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": 999})
	assert response.status_code == 404
	print("   ✅ 404 오류 정상 반환")
	
	# 4. 다른 이벤트의 메뉴에 투표 시도
	print("❌ Test 4: 다른 이벤트의 메뉴에 투표")
	# 두 번째 이벤트와 메뉴 생성
	event2_response = client.post("/api/events", json={"name": "다른 이벤트"})
	assert event2_response.status_code == 201
	event2_id = event2_response.json()["event_id"]
	
	menu_response = client.post(f"/api/events/{event2_id}/menus", json={"name": "다른 메뉴"})
	assert menu_response.status_code == 201
	menu_id = menu_response.json()["id"]
	
	# 첫 번째 이벤트에서 두 번째 이벤트의 메뉴에 투표 시도
	response = client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu_id})
	assert response.status_code == 400
	print("   ✅ 400 오류 정상 반환")
	
	# 5. 잘못된 데이터 형식 테스트
	print("❌ Test 5: 잘못된 데이터 형식")
	
	# 메뉴 생성 시 name 필드 누락
	response = client.post(f"/api/events/{event_id}/menus", json={})
	assert response.status_code == 422
	print("   ✅ 메뉴 생성 시 필수 필드 누락 422 오류")
	
	# 투표 시 menu_id 필드 누락
	response = client.post(f"/api/events/{event_id}/votes", json={})
	assert response.status_code == 422
	print("   ✅ 투표 시 필수 필드 누락 422 오류")
	
	print("\n✅ 포괄적인 오류 처리 테스트 성공!")
	print("=" * 60)
