#!/bin/bash
# Install memanto daily sync as system cron job
# Run: sudo bash scripts/install-memanto-cron.sh

SCRIPT_PATH="/home/node/.openclaw/workspace/skills/memanto_sync/run.sh"
CRON_LINE="0 4 * * * $SCRIPT_PATH sync >> /home/node/.openclaw/workspace/logs/memanto_sync.log 2>&1"

# Add to root's crontab
( crontab -l 2>/dev/null | grep -v "memanto_sync" ; echo "$CRON_LINE" ) | crontab -

echo "✅ Installed memanto daily sync cron:"
echo "   $CRON_LINE"
echo ""
echo "Verify with: crontab -l | grep memanto"
