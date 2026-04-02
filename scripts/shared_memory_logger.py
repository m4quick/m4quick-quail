#!/usr/bin/env python3
"""
Shared Memory Logger - Auto-log all conversations for cross-instance sync
Usage: Import and call log_message() from any OpenClaw instance
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

LOG_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "shared_conversation.jsonl"

def normalize_entry(entry):
    """Normalize various entry formats to standard format."""
    # Handle shell syntax in JSON (Inanna's format)
    if isinstance(entry, str):
        # Try to extract message from malformed JSON
        msg_match = re.search(r'"message":\s*"([^"]*)"', entry)
        time_match = re.search(r'"timestamp":\s*"([^"]*)"', entry)
        
        return {
            "time": time_match.group(1) if time_match else datetime.now().isoformat(),
            "instance": "inanna",
            "speaker": "inanna",
            "msg": msg_match.group(1) if msg_match else entry[:500]
        }
    
    # Standardize field names
    normalized = {
        "time": entry.get("time") or entry.get("timestamp") or datetime.now().isoformat(),
        "instance": entry.get("instance") or entry.get("instance_id") or "unknown",
        "speaker": entry.get("speaker") or entry.get("from") or "unknown",
        "msg": entry.get("msg") or entry.get("message") or str(entry)[:500]
    }
    
    return normalized

def log_message(speaker: str, msg: str, instance_id: str = None):
    """Log a message to shared conversation file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "time": datetime.now().isoformat(),
        "instance": instance_id or "enki",
        "speaker": speaker,
        "msg": msg[:500]  # Limit length
    }
    
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
        
def read_all_entries():
    """Read all entries, normalizing various formats."""
    if not LOG_FILE.exists():
        return []
    
    entries = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(normalize_entry(entry))
            except json.JSONDecodeError:
                # Try to salvage malformed entries
                entries.append(normalize_entry(line))
    
    return entries

def get_recent_context(hours: int = 24, limit: int = 50) -> str:
    """Get recent conversation as formatted text for system prompt."""
    if not LOG_FILE.exists():
        return "No shared conversation history yet."
    
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(hours=hours)
    
    entries = []
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                entry_time = datetime.fromisoformat(entry['time'])
                if entry_time >= cutoff:
                    entries.append(entry)
    except (json.JSONDecodeError, ValueError):
        pass
    
    if not entries:
        return "No recent conversations."
    
    lines = ["## Recent Cross-Instance Conversations", ""]
    for entry in entries[-limit:]:
        time_str = entry['time'][11:16]  # HH:MM
        lines.append(f"[{time_str}] {entry['speaker']}: {entry['msg']}")
    
    return '\n'.join(lines)

if __name__ == '__main__':
    # Test
    print(get_recent_context())
