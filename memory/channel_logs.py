#!/usr/bin/env python3
"""
Channel Log System - Cross-channel memory for OpenClaw
Logs all conversations from each channel so any instance can reference them.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

WORKSPACE = Path.home() / ".openclaw" / "workspace"
LOGS_DIR = WORKSPACE / "memory" / "channel_logs"


def ensure_logs_dir():
    """Create logs directory if needed."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log_message(channel: str, sender: str, message: str, 
                instance_id: Optional[str] = None) -> Path:
    """Log a message from any channel.
    
    Args:
        channel: e.g., 'telegram', 'tui', 'webui', 'webchat'
        sender: username or 'user' / 'assistant'
        message: the message content
        instance_id: optional unique ID for the conversation session
    """
    ensure_logs_dir()
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"{today}_{channel}.jsonl"
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "channel": channel,
        "sender": sender,
        "message": message,
        "instance_id": instance_id or "unknown"
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    return log_file


def get_recent_logs(channel: Optional[str] = None, 
                   hours: int = 24,
                   limit: int = 50) -> list:
    """Get recent log entries.
    
    Args:
        channel: Filter by channel (None = all)
        hours: How many hours back to look
        limit: Max entries to return
    """
    ensure_logs_dir()
    
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(hours=hours)
    
    entries = []
    
    # Find log files
    log_files = sorted(LOGS_DIR.glob("*.jsonl"), reverse=True)
    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    if entry_time < cutoff:
                        continue
                    
                    if channel and entry['channel'] != channel:
                        continue
                    
                    entries.append(entry)
                    
                    if len(entries) >= limit:
                        break
                        
        except (json.JSONDecodeError, ValueError):
            continue
    
    return entries


def search_logs(query: str, hours: int = 168) -> list:
    """Search logs for specific content.
    
    Args:
        query: Text to search for (case-insensitive)
        hours: How many hours back to search (default 1 week)
    """
    entries = get_recent_logs(hours=hours, limit=1000)
    query_lower = query.lower()
    
    return [e for e in entries if query_lower in e['message'].lower()]


def summarize_recent(channel: Optional[str] = None, 
                    hours: int = 24) -> str:
    """Get a text summary of recent conversations.
    
    Useful for spawning context: 'What did we discuss recently?'
    """
    entries = get_recent_logs(channel=channel, hours=hours)
    
    if not entries:
        return "No recent conversations found."
    
    lines = []
    lines.append(f"Recent conversations (last {hours}h):")
    lines.append("=" * 50)
    
    for entry in entries[-20:]:  # Last 20 messages
        time_str = entry['timestamp'][11:16]  # HH:MM
        lines.append(f"[{time_str}] {entry['channel']} | {entry['sender']}: {entry['message'][:100]}")
    
    return '\n'.join(lines)


def main():
    """CLI for reviewing logs."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Channel Log System')
    parser.add_argument('--recent', '-r', action='store_true', 
                       help='Show recent conversations')
    parser.add_argument('--channel', '-c', help='Filter by channel')
    parser.add_argument('--hours', '-H', type=int, default=24,
                       help='Hours back to look')
    parser.add_argument('--search', '-s', help='Search for text')
    parser.add_argument('--summary', '-S', action='store_true',
                       help='Show summary only')
    
    args = parser.parse_args()
    
    if args.search:
        results = search_logs(args.search, hours=args.hours)
        print(f"Found {len(results)} matches for '{args.search}':")
        for entry in results:
            print(f"[{entry['timestamp']}] {entry['channel']}: {entry['message'][:80]}")
    
    elif args.summary or args.recent:
        print(summarize_recent(channel=args.channel, hours=args.hours))
    
    else:
        # Show available logs
        ensure_logs_dir()
        files = sorted(LOGS_DIR.glob("*.jsonl"))
        print(f"Available log files ({len(files)} total):")
        for f in files[-10:]:  # Last 10 days
            size = f.stat().st_size
            print(f"  {f.name} ({size/1024:.1f} KB)")


if __name__ == '__main__':
    main()
