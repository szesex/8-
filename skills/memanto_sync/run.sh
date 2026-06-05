#!/bin/bash
# Memanto sync wrapper - sets API key from env file if not set
export MOORCHEH_API_KEY="2rJhqS0lFm9XlWKMEhX2jqbU4lFR85C5Oaxejxrj"
exec python3 -u /home/node/.openclaw/workspace/skills/memanto_sync/memanto_sync.py "$@"
