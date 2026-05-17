#!/usr/bin/env python3
"""
Bazi Cron Daemon - Standalone scheduler
Runs as background process, triggers bazi alert/feedback at set times.
"""
import datetime
import os
import sys
import time
import subprocess
import json
from pathlib import Path

WORKSPACE = "/home/node/.openclaw/workspace"
STATE_DIR = "/home/node/.openclaw/workspace/state"
LOG_DIR = "/home/node/.openclaw/workspace/logs"
PID_FILE = "/home/node/.openclaw/workspace/bazi_cron.pid"

# HKT timezone offset
HKT_OFFSET_HOURS = 8

def get_hkt_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=HKT_OFFSET_HOURS)

def is_hkt_time(hour, minute):
    now = get_hkt_now()
    return now.hour == hour and now.minute == minute

def ensure_dirs():
    for d in [STATE_DIR, LOG_DIR]:
        os.makedirs(d, exist_ok=True)

def run_script(name):
    """Run bazi skill script and capture output."""
    script_path = os.path.join(WORKSPACE, f"bazi_skill_v2.py")
    log_file = os.path.join(LOG_DIR, f"bazi-{name}.log")
    
    try:
        with open(log_file, "a") as f:
            f.write(f"\n=== {datetime.datetime.now().isoformat()} ===\n")
            result = subprocess.run(
                ["python3", script_path, name],
                capture_output=True,
                text=True,
                timeout=60
            )
            f.write(result.stdout)
            if result.stderr:
                f.write(f"STDERR: {result.stderr}\n")
        return True
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"ERROR: {e}\n")
        return False

def send_telegram(message):
    """Send message via OpenClaw's message tool functionality using message tool."""
    # This will be handled by the cron job runner in OpenClaw itself
    # For now, we just log - actual sending is done by the Python script output
    pass

def already_sent_today(name):
    """Check if we've already run today."""
    state_file = os.path.join(STATE_DIR, f"{name}_last_sent.json")
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                data = json.load(f)
                last_date = data.get("last_sent", "")
                today = get_hkt_now().strftime("%Y-%m-%d")
                return last_date == today
        except:
            pass
    return False

def mark_sent_today(name):
    """Record that we've run today."""
    state_file = os.path.join(STATE_DIR, f"{name}_last_sent.json")
    with open(state_file, "w") as f:
        json.dump({"last_sent": get_hkt_now().strftime("%Y-%m-%d")}, f)

def main():
    ensure_dirs()
    
    # Check if already running
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            # Check if process exists
            os.kill(pid, 0)
            print(f"Already running with PID {pid}")
            sys.exit(0)
        except (ValueError, ProcessLookupError):
            pass
    
    # Write PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    
    print(f"Bazi Cron Daemon started at {datetime.datetime.now().isoformat()}")
    
    last_check = {}
    
    while True:
        now = get_hkt_now()
        current_hour = now.hour
        current_min = now.minute
        
        # Check schedules:
        # Alert: HKT 07:30 (UTC 23:30)
        # Feedback: HKT 23:00 (UTC 15:00)
        
        check_times = {
            "alert": (7, 30),   # HKT 07:30
            "feedback": (23, 0) # HKT 23:00
        }
        
        for name, (target_hour, target_min) in check_times.items():
            key = f"{name}_{target_hour:02d}{target_min:02d}"
            
            if current_hour == target_hour and current_min == target_min:
                if key != last_check.get(name):
                    print(f"Triggering {name} at {now.isoformat()}")
                    if not already_sent_today(name):
                        success = run_script(name)
                        if success:
                            mark_sent_today(name)
                            print(f"{name} completed successfully")
                        else:
                            print(f"{name} failed")
                    else:
                        print(f"{name} already sent today, skipping")
                    last_check[name] = key
            else:
                # Reset check flag when minute changes
                if key in last_check:
                    del last_check[name]
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    main()