#!/bin/bash
# Memanto sync wrapper - sets API key from env file and ensures PATH includes /usr/local/bin
export MOORCHEH_API_KEY="2rJhqS0lFm9XlWKMEhX2jqbU4lFR85C5Oaxejxrj"
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
exec python3 -u /home/node/.openclaw/workspace/skills/memanto_sync/memanto_sync.py "$@"
