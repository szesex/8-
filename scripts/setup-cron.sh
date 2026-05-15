#!/bin/bash
# OpenClaw Bazi Cron Setup

# Create logs directory
mkdir -p /home/node/.openclaw/workspace/logs

# Write cron file
cat > /tmp/bazi-cron.txt << 'CRONEOF'
# OpenClaw Bazi Cron Jobs
# Alert: HKT 07:30
30 23 * * * cd /home/node/.openclaw/workspace && python3 bazi_skill_v2.py alert >> /home/node/.openclaw/workspace/logs/bazi-alert.log 2>&1

# Feedback: HKT 23:00 (UTC 15:00)
0 15 * * * cd /home/node/.openclaw/workspace && python3 bazi_skill_v2.py feedback >> /home/node/.openclaw/workspace/logs/bazi-feedback.log 2>&1
CRONEOF

# Install crontab
crontab /tmp/bazi-cron.txt

# Verify
echo "=== Installed crontab ==="
crontab -l
echo "=== Done ==="