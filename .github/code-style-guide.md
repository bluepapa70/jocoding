# 코드 스타일 가이드

## 개요

회식 메뉴 투표 시스템의 통합 코드 스타일 가이드입니다.
모든 개발자와 AI 도구가 일관된 코드 스타일을 유지하기 위한 규칙을 정의합니다.

---

## 일반 원칙

### 1. 가독성 우선
- 코드는 작성하는 시간보다 읽는 시간이 더 많습니다.
- 명확하고 이해하기 쉬운 코드를 작성합니다.
- 복잡한 로직은 주석으로 설명합니다.

### 2. 일관성 유지
- 프로젝트 전체에서 동일한 스타일을 사용합니다.
- 기존 코드의 스타일을 따릅니다.

### 3. 단순성 추구
- KISS(Keep It Simple, Stupid) 원칙을 따릅니다.
- 불필요한 복잡성을 피합니다.

---

## Python 스타일 가이드

본 프로젝트는 **PEP 8** 스타일 가이드를 준수합니다.

### 1. 들여쓰기 및 공백

#### 들여쓰기
```python
# 탭(Tab) 사용 — 스페이스 금지
def create_event(name: str) -> Event:
	"""이벤트를 생성한다."""
	return Event(name=name)
```

#### 줄 길이
- 최대 79자 이내 권장

#### 중괄호/괄호 스타일
```python
# 여러 인자는 줄바꿈 후 탭 들여쓰기
result = some_function(
	argument_one,
	argument_two,
	argument_three,
)
```

### 2. 명명 규칙

#### 변수명 / 함수명
```python
# snake_case 사용
event_id: int
menu_name: str

def get_event_by_id(event_id: int) -> Event:
	pass
```

#### 클래스명
```python
# PascalCase 사용
class EventService:
	pass

class MenuRepository:
	pass
```

#### 상수
```python
# UPPER_SNAKE_CASE 사용
DATABASE_URL = "sqlite:///./vote.db"
```

### 3. 타입 힌트

모든 함수와 메서드에 타입 힌트를 필수로 추가합니다.

```python
from typing import List, Optional

def get_menus(event_id: int) -> List[Menu]:
	"""이벤트별 메뉴 목록을 반환한다."""
	pass

def find_event(event_id: int) -> Optional[Event]:
	"""이벤트를 조회한다. 없으면 None 반환."""
	pass
```

### 4. Docstring (PEP 257)

함수/클래스/메서드에 docstring을 필수로 작성합니다.

```python
def calculate_vote_count(menu_id: int) -> int:
	"""
	특정 메뉴의 투표 수를 계산한다.

	Parameters:
		menu_id (int): 조회할 메뉴 ID.

	Returns:
		int: 해당 메뉴의 총 투표 수.
	"""
	pass
```

### 5. 주석 스타일

```python
# 단일 줄 주석은 # 뒤에 한 칸 공백
x = x + 1  # 카운터 증가

# TODO: 향후 중복 투표 방지 로직 추가
# FIXME: 동시성 처리 필요
```

---

## 프로젝트 아키텍처 규칙

### 계층 간 의존 방향 (단방향)
```
api → service → repository → models
              ↘             ↗
                schemas(DTO)
```

- **api**: Router만 포함, 비즈니스 로직 금지
- **service**: 비즈니스 로직만, DB 직접 접근 금지
- **repository**: DB CRUD만, 비즈니스 로직 금지
- **models**: SQLAlchemy ORM 테이블 정의
- **schemas**: Pydantic DTO (입력/출력 모델)

### 필수 파일
- **모든 폴더에 `__init__.py` 필수**

---

## 보안 코딩

상세 내용은 **`.github/instructions/security-and-owasp.instructions.md`** 참조

### 주요 원칙
- SQLAlchemy ORM 파라미터 바인딩만 사용 (raw SQL 금지)
- 모든 API 입력값은 Pydantic 스키마로 검증
- 에러 응답 시 내부 구현 세부사항 미노출

---

## 에러 처리

상세 내용은 **`.github/instructions/`** 참조

### 기본 패턴
```python
from fastapi import HTTPException

def get_event_or_404(event_id: int) -> Event:
	"""이벤트를 조회하고 없으면 404를 반환한다."""
	event = event_repository.find(event_id)
	if not event:
		raise HTTPException(status_code=404, detail="Event not found")
	return event
```

---

## 참고 자료

- [PEP 8 — Python 스타일 가이드](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring 컨벤션](https://peps.python.org/pep-0257/)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.x 문서](https://docs.sqlalchemy.org/en/20/)

---

**마지막 업데이트**: 2026-04-21
**문서 버전**: 1.0
**적용 범위**: 회식 메뉴 투표 시스템 전체
