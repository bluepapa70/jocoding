---
mode: agent
description: '문제 해결을 위한 솔루션을 구현합니다.'
tools: ['changes', 'codebase', 'editFiles', 'fetch', 'findTestFiles', 'openSimpleBrowser', 'problems', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI']
---

모든 **유효한 입력**에 대해 올바르게 동작하는 **고품질 범용 솔루션**을 작성하십시오.  
테스트 케이스에만 맞춰 하드코딩하거나 특정 입력에서만 동작하는 코드를 작성하지 마십시오.  
문제를 일반적으로 해결할 수 있는 **실제 알고리즘**을 구현해야 합니다.

> **중요:**  
> 테스트는 정답을 가리키는 힌트가 아니라, 구현의 **정확성 검증용**입니다.  
> 문제 요구 사항을 먼저 깊이 이해하고, 올바른 알고리즘과 설계를 적용하세요.

- 값이나 조건을 하드코딩하지 말고, **확장 가능**하고 **유지 보수**가 쉬운 코드를 작성하십시오.  
- 과제 자체가 **비현실적이거나 지나치게 어렵다**고 판단되거나, **테스트가 잘못되었다**고 의심될 경우 그 사실을 알려주십시오.  
- 최종 솔루션은 **견고하고, 유지 보수 가능하며, 확장 가능**해야 합니다.


## 테스트 및 검증 절차

테스트를 실행하거나 작업 완료를 선언하기 전에, 아래 정적 분석을 반드시 통과해야 합니다!

가상환경 설정 후 아래 지침을 따르십시오:
```
source .venv/bin/activate
```

1. ALWAYS: ruff check . 을 실행해 모든 린트 오류를 수정한다.
2. ALWAYS: mypy app/ 로 모든 타입 오류를 해결한다.
3. NEVER: ruff 또는 mypy 오류가 있으면 pytest 를 절대 실행하지 않는다.
4. FIX: 문제를 모두 고친 후에만 테스트를 진행한다.

## 테스트 및 검증 절차

- 테스트: pytest -v