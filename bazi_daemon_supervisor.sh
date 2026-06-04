#!/bin/bash
# Bazi daemon supervisor - auto-restarts on crash
# Usage: ./bazi_daemon_supervisor.sh

set -e
DAEMON="/home/node/.openclaw/workspace/bazi_cron_daemon.py"
LOG="/home/node/.openclaw/workspace/logs/bazi-daemon-supervisor.log"
PIDFILE="/home/node/.openclaw/workspace/bazi_cron.pid"

log() {
  echo "[$(date -Iseconds)] $*" >> "$LOG"
}

cleanup_pid() {
  if [ -f "$PIDFILE" ]; then
    OLD_PID=$(cat "$PIDFILE" 2>/dev/null || echo "")
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
      kill "$OLD_PID" 2>/dev/null || true
      sleep 1
      kill -9 "$OLD_PID" 2>/dev/null || true
    fi
    rm -f "$PIDFILE"
  fi
}

trap 'cleanup_pid; exit 0' SIGINT SIGTERM

log "Supervisor starting"
cleanup_pid

while true; do
  log "Starting daemon"
  python3 -u "$DAEMON" >> "$LOG" 2>&1
  EXIT_CODE=$?
  log "Daemon exited with code $EXIT_CODE, restarting in 5s..."
  sleep 5
done
