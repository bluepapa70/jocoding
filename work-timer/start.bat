@echo off
:: 업무 타이머 실행 스크립트 (Windows)

set DIR=%~dp0
set FILE=%DIR%work-timer.html

if not exist "%FILE%" (
  echo 오류: work-timer.html 파일을 찾을 수 없습니다.
  pause
  exit /b 1
)

echo 업무 타이머를 시작합니다...

:: Chrome 전체화면 앱 모드로 실행 시도
set CHROME="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
if exist %CHROME% (
  start "" %CHROME% --start-fullscreen --app="file:///%FILE:\=/%"
  goto :end
)

:: Edge 시도
set EDGE="%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"
if exist %EDGE% (
  start "" %EDGE% --start-fullscreen --app="file:///%FILE:\=/%"
  goto :end
)

:: 기본 브라우저로 열기
start "" "%FILE%"

:end
