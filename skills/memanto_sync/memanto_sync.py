#!/usr/bin/env python3
"""
Memanto Sync Skill for OpenClaw
Syncs workspace memory (MEMORY.md + memory/*.md) to Memanto cloud storage.

Usage:
    python3 memanto_sync.py sync       # Sync all memory to memanto
    python3 memanto_sync.py recall Q   # Query memanto
    python3 memanto_sync.py status     # Show memanto status
    python3 memanto_sync.py watch      # Watch mode (sync on change)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = "/home/node/.openclaw/workspace"
MEMORY_FILE = f"{WORKSPACE}/MEMORY.md"
MEMORY_DIR = f"{WORKSPACE}/memory"

# Load MOORCHEH_API_KEY from env or config
def get_api_key():
    key = os.environ.get("MOORCHEH_API_KEY", "").strip()
    if not key:
        # Try reading from memanto config
        config_dir = Path.home() / ".memanto"
        env_file = config_dir / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("MOORCHEH_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def run_memanto(args, env=None):
    """Run a memanto CLI command and return output."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    if "MOORCHEH_API_KEY" not in full_env:
        key = get_api_key()
        if key:
            full_env["MOORCHEH_API_KEY"] = key
    try:
        result = subprocess.run(
            ["memanto"] + args,
            capture_output=True,
            text=True,
            env=full_env,
            timeout=30,
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def chunk_text(text, max_chars=500):
    """Split long text into chunks of max_chars, preserving line boundaries."""
    if len(text) <= max_chars:
        return [text]
    chunks = []
    current = []
    current_len = 0
    for line in text.split("\n"):
        if current_len + len(line) + 1 > max_chars and current:
            chunks.append("\n".join(current))
            current = [line]
            current_len = len(line)
        else:
            current.append(line)
            current_len += len(line) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks


def sync_memory():
    """Sync MEMORY.md + memory/*.md to memanto."""
    api_key = get_api_key()
    if not api_key:
        print("❌ MOORCHEH_API_KEY not set. Run: memanto config set-key <key>")
        return 1

    # Collect all memory files
    files_to_sync = []
    if os.path.exists(MEMORY_FILE):
        files_to_sync.append(MEMORY_FILE)
    if os.path.exists(MEMORY_DIR):
        for f in sorted(Path(MEMORY_DIR).glob("*.md")):
            files_to_sync.append(str(f))

    if not files_to_sync:
        print("⚠️  No memory files found")
        return 0

    print(f"📁 Found {len(files_to_sync)} memory file(s)")

    total_stored = 0
    total_failed = 0

    for file_path in files_to_sync:
        rel_path = file_path.replace(WORKSPACE + "/", "")
        print(f"\n📄 Syncing {rel_path}...")

        try:
            content = Path(file_path).read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ❌ Read error: {e}")
            total_failed += 1
            continue

        # Chunk the content
        chunks = chunk_text(content, max_chars=500)
        if len(chunks) > 100:
            print(f"  ⚠️  Too many chunks ({len(chunks)}), truncating to 100")
            chunks = chunks[:100]
        print(f"  → {len(chunks)} chunk(s)")

        for i, chunk in enumerate(chunks):
            # Prefix with source label
            memory_text = f"[{rel_path}#{i+1}/{len(chunks)}] {chunk}"
            try:
                rc, stdout, stderr = run_memanto(["remember", memory_text])
                if rc == 0:
                    total_stored += 1
                else:
                    print(f"  ❌ Chunk {i+1} failed: {stderr[:100]}")
                    total_failed += 1
                # Rate limit: 200ms between calls (~5 calls/sec)
                import time
                time.sleep(0.2)
            except Exception as e:
                print(f"  ❌ Chunk {i+1} error: {e}")
                total_failed += 1

    print(f"\n✅ Sync complete: {total_stored} stored, {total_failed} failed")
    return 0 if total_failed == 0 else 1


def recall_query(query):
    """Query memanto and print results."""
    api_key = get_api_key()
    if not api_key:
        print("❌ MOORCHEH_API_KEY not set")
        return 1
    rc, stdout, stderr = run_memanto(["recall", query])
    print(stdout)
    if stderr:
        print(f"[stderr]: {stderr}")
    return rc


def show_status():
    """Show memanto status."""
    rc, stdout, stderr = run_memanto(["status"])
    print(stdout)
    if stderr:
        print(f"[stderr]: {stderr}")
    return rc


def watch_mode():
    """Watch memory files and sync on change."""
    import time
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class MemoryHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory:
                return
            if event.src_path.endswith(".md"):
                print(f"\n🔄 Change detected: {event.src_path}")
                sync_memory()

    handler = MemoryHandler()
    observer = Observer()
    observer.schedule(handler, WORKSPACE, recursive=True)
    observer.start()
    print(f"👀 Watching {WORKSPACE} for changes... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(description="Memanto Sync Skill for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("sync", help="Sync all memory to memanto")
    recall_p = subparsers.add_parser("recall", help="Query memanto")
    recall_p.add_argument("query", nargs="+", help="Search query")
    subparsers.add_parser("status", help="Show memanto status")
    subparsers.add_parser("watch", help="Watch mode (sync on file change)")

    args = parser.parse_args()

    if args.command == "sync":
        return sync_memory()
    elif args.command == "recall":
        return recall_query(" ".join(args.query))
    elif args.command == "status":
        return show_status()
    elif args.command == "watch":
        return watch_mode()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
