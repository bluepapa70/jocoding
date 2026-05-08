# 커밋 메시지 스타일 가이드

## Format

커밋 메시지 형식(Conventional Commits 스타일)은 아래와 같습니다.

### 기본 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 상세 형식 (이슈 트래킹 포함)

```
[문제의 원인]

    문제가 발생한 원인 또는 수정이 필요한 이유를 구체적으로 기술

[수정 사항]

    변경된 내용 및 수정 방법을 명확하게 기술

[변경된 파일/모듈]

    변경된 모든 파일/디렉터리 목록
    예) app/service/menu_service.py

[테스트 사항]

테스트 환경 : Python 3.x, pytest, SQLite in-memory

Test Step)
    1. pytest 실행: python -m pytest -q .
    2. 결과 확인: 모든 테스트 PASS
    3. 예상 결과: 0 failed
```

---

## Type 종류

| Type | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | feat(menu): 메뉴 후보 제안 API 추가 |
| `fix` | 버그 수정 | fix(vote): 중복 투표 방지 로직 수정 |
| `test` | 테스트 추가/수정 | test(event): 이벤트 생성 실패 케이스 추가 |
| `refactor` | 리팩토링 | refactor(service): 공통 조회 로직 분리 |
| `docs` | 문서 변경 | docs: README 업데이트 |
| `style` | 코드 포맷팅 (기능 변경 없음) | style: 들여쓰기 수정 |
| `chore` | 빌드/설정 변경 | chore: 의존성 업데이트 |
| `perf` | 성능 개선 | perf: 투표 결과 쿼리 최적화 |
| `security` | 보안 관련 수정 | security: SQL 인젝션 방지 로직 강화 |

---

## Scope 종류 (프로젝트별)

| Scope | 설명 |
|-------|------|
| `event` | 회식 이벤트 관련 |
| `menu` | 메뉴 후보 관련 |
| `vote` | 투표 관련 |
| `result` | 투표 결과 관련 |
| `infra` | DB, 서버 설정 등 인프라 |
| `test` | 테스트 코드 |
| `docs` | 문서 |

---

## 작성 규칙

### Subject (제목)
- 50자 이내로 작성
- 마침표 없이 끝냄
- 명령형으로 작성 (한글: "추가", "수정", "변경")

### Body (본문)
- 선택 사항 (필요시 작성)
- "무엇을" 보다 "왜"에 초점
- 72자마다 줄바꿈 권장

### Footer (꼬리말)
- 이슈 참조: `Closes #123`, `Fixes #456`
- Breaking Change: `BREAKING CHANGE: 설명`

---

## TDD 사이클 커밋 예시

```
test(menu): 메뉴 목록 조회 빈 리스트 반환 테스트 추가
```
```
feat(menu): 이벤트별 메뉴 목록 조회 서비스 구현
```
```
refactor(menu): 메뉴 서비스 중복 조회 로직 제거
```

---

## 예시

### 기능 추가
```
feat(vote): 이벤트별 메뉴 투표 API 추가

- POST /api/events/{event_id}/votes 엔드포인트 구현
- 투표 서비스 및 레포지토리 계층 추가
- 투표 Pydantic 스키마 정의

Closes #12
```

### 버그 수정
```
fix(event): 이벤트 ID 없을 때 500 대신 404 반환

존재하지 않는 event_id 조회 시 KeyError가 발생하여
서버 에러로 응답하는 문제 수정.

HTTPException(status_code=404)으로 올바르게 처리.

Fixes #34
```

---

**마지막 업데이트**: 2026-04-21
**문서 버전**: 1.0
**적용 범위**: 회식 메뉴 투표 시스템 전체
