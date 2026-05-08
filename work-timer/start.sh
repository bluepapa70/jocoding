#!/bin/bash
# 업무 타이머 실행 스크립트

DIR="$(cd "$(dirname "$0")" && pwd)"
FILE="$DIR/work-timer.html"

if [ ! -f "$FILE" ]; then
  echo "오류: work-timer.html 파일을 찾을 수 없습니다."
  exit 1
fi

echo "업무 타이머를 시작합니다..."

# OS 감지 후 브라우저 전체화면으로 실행
case "$(uname)" in
  Darwin)
    # macOS — Chrome 전체화면
    if command -v "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" &>/dev/null; then
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        --start-fullscreen --app="file://$FILE" &
    else
      open "$FILE"
    fi
    ;;
  Linux)
    if command -v google-chrome &>/dev/null; then
      google-chrome --start-fullscreen --app="file://$FILE" &
    elif command -v chromium-browser &>/dev/null; then
      chromium-browser --start-fullscreen --app="file://$FILE" &
    else
      xdg-open "$FILE"
    fi
    ;;
  *)
    echo "Windows는 start.bat을 사용하세요."
    ;;
esac
