# 회식 메뉴 정하기 백엔드 Copilot Instructions

## Project Overview

본 프로젝트는 익명의 참여자들이 특정 회식 이벤트에 대한 메뉴 후보를 제안하고, 투표하며, 그 결과를 확인할 수 있는 FastAPI 기반의 백엔드 시스템입니다.

호스트가 회식 이벤트를 생성하고, 참여자들이 메뉴 후보를 제안할 수 있으며, 각 참여자는 자신이 선호하는 메뉴에 투표할 수 있습니다. 최종적으로 가장 많은 투표를 받은 메뉴가 회식 메뉴로 선정됩니다.

사용자는 회식 메뉴 후보를 제안하고, 투표를 통해 선호하는 메뉴를 선택할 수 있으며, 최종적으로 가장 많은 투표를 받은 메뉴가 회식 메뉴로 선정됩니다.

Layered architecture로 구성되어 있으며, 각 계층은 다음과 같은 역할을 수행합니다:

### Root Folders

- `app/`: FastAPI 앱 (routers, models, schemas)
- `test/`: Integration tests and test infrastructure

### Core Architecture (`app/` folder)

- `app/api/`: FastAPI Routers (프레젠테이션)
- `app/service/`: 비즈니스 로직 (애플리케이션)
- `app/repository/`: DB 접근 계층 (SQLite 사용)
- `app/models/`: SQLAlchemy ORM (도메인)
- `app/schemas/`: Pydantic DTO (전송 객체)

### 가상 환경

본 프로젝트는 Python 가상 환경으로 `.venv` 디렉토리를 사용합니다. 모든 패키지 설치 및 실행은 `.venv` 환경에서 이루어져야 합니다.

```
source .venv/bin/activate
```

### Finding Related Code

1. **먼저 시맨틱 검색**: 일반적인 개념을 파일 검색으로 찾으세요.
2. **정확한 문자열은 grep 사용**: 에러 메시지나 특정 함수명을 grep으로 찾으세요.
3. **import 따라가기**: 문제가 되는 모듈을 import하는 파일을 확인하세요.
4. **테스트 파일 확인**: 사용 패턴과 기대 동작을 자주 보여줍니다.


## TDD

본 프로젝트는 TDD(Test-Driven Development) 방식을 따릅니다. 새로운 기능을 추가하거나 버그를 수정하기 전에 반드시 테스트 케이스를 먼저 작성해야 하며, 모든 테스트는 `pytest`를 사용하여 실행합니다.

- 항상 "Red - Green - Refactor" 순서로 개발을 진행하세요.
- 최대한 다양한 유저 스토리를 반영해 구체적으로 테스트 케이스를 작성합니다.
- Test 함수명 아래에 docstring을 작성하여 테스트의 목적과 기대 결과를 명확히 합니다.
- conftest.py에 fixture(autouse=True)를 사용하여 테스트 전후에 필요한 초기화 작업을 수행합니다.
- 아래와 같이 Given-When-Then 패턴을 사용하여 테스트 케이스를 작성합니다.

```
def test_menu_list_empty():
    """
    메뉴가 없을 때 빈 리스트를 반환해야 한다.
    """
    # Given: 데이터베이스에 메뉴가 없는 상태

    # When: /api/menus 엔드포인트에 GET 요청을 보낸다
    response = client.get("/api/menus")

    # Then: 200 OK와 빈 리스트가 반환된다
    assert response.status_code == 200
    assert response.json() == []
```

## Coding Guidelines

### Indentation

탭(tab)을 사용하고, 스페이스(space)는 사용하지 않습니다.

### Type Hints

모든 함수와 메서드에 타입 힌트를 추가하세요.

### 코드 품질

- 새로운 구조를 만들기 전에 기존 코드 패턴을 확인하세요
- 반복을 위해 임시로 생성한 새 파일, 스크립트, 헬퍼 파일은 작업이 끝나면 반드시 삭제하세요
- ALWAYS: 모든 폴더에 init.py 파일이 존재해야 합니다.

## Testing and Validation

TestClient 를 사용하여 FastAPI 앱을 테스트합니다. 모든 테스트는 `pytest`를 사용하여 실행됩니다.