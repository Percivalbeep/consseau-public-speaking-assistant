#!/bin/zsh
cd "$(dirname "$0")" || exit 1
if ! curl --noproxy '*' -fsS http://127.0.0.1:8766/teacher >/dev/null 2>&1; then
  mkdir -p .work
  nohup /usr/bin/python3 tools/teacher_server.py >> .work/teacher-server.log 2>&1 < /dev/null &!
fi
for attempt in {1..20}; do
  if curl --noproxy '*' -fsS http://127.0.0.1:8766/teacher >/dev/null 2>&1; then
    open http://127.0.0.1:8766/teacher
    exit 0
  fi
  sleep 0.5
done
echo '启动失败，请检查 .work/teacher-server.log。'
read -k 1
