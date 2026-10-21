#!/bin/bash
# Usage: archive_after_send.sh <category> <date YYYY-MM-DD> <time HH:MM> <title> <body-file> [image]
# Failure-tolerant: always exits 0; logs to /workspace/push-site/archive.log
L=/workspace/push-site/archive.log
{
  echo "$(date '+%F %T') archive $1 $2 $3"
  args=(--category "$1" --date "$2" --time "$3" --title "$4" --body-file "$5")
  [ -n "$6" ] && [ -f "$6" ] && args+=(--image "$6")
  timeout 300 python3 /workspace/push-site/add_push.py "${args[@]}" || echo "archive FAILED rc=$?"
} >>"$L" 2>&1
exit 0
