#!/bin/zsh
cd "$(dirname "$0")" || exit 1
if curl --noproxy '*' -fsS http://127.0.0.1:8766/teacher >/dev/null 2>&1; then
  open http://127.0.0.1:8766/teacher
  exit 0
fi
python3 tools/teacher_server.py &
studio_pid=$!
trap 'kill "$studio_pid" 2>/dev/null' EXIT INT TERM
open http://127.0.0.1:8766/teacher
echo '教师工作台已启动。使用期间请保留此窗口；关闭窗口后本机生成功能会停止。'
wait "$studio_pid"
