#!/usr/bin/env python3
"""
Context Bridge - Phase 2.3
Maintain persistent context across sessions and platforms

Usage:
    python3 memory/context_bridge.py --get "last_topic"
    python3 memory/context_bridge.py --set "last_topic" "Pi-hole monitoring"
    python3 memory/context_bridge.py --summary
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
CONTEXT_FILE = MEMORY_DIR / "context_bridge.json"


def load_context():
    """Load current context."""
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE) as f:
            return json.load(f)
    return {
        'sessions': [],
        'topics': {},
        'pending_actions': [],
        'last_session_end': None,
        'version': 1
    }


def save_context(data):
    """Save context."""
    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def start_session(platform="webchat"):
    """Record new session start."""
    ctx = load_context()
    
    session = {
        'started': datetime.now().isoformat(),
        'platform': platform,
        'topic_continuity': detect_topic_continuity(ctx)
    }
    
    ctx['sessions'].append(session)
    
    # Keep only last 50 sessions
    ctx['sessions'] = ctx['sessions'][-50:]
    
    save_context(ctx)
    
    # Return context for this session
    return {
        'session_started': session['started'],
        'continuing_from': ctx.get('last_topic'),
        'pending_actions': ctx.get('pending_actions', []),
        'greeting': generate_contextual_greeting(ctx)
    }


def detect_topic_continuity(ctx):
    """Detect if we're continuing a previous topic."""
    if not ctx.get('last_session_end'):
        return None
    
    last_end = datetime.fromisoformat(ctx['last_session_end'])
    gap = datetime.now() - last_end
    
    # If less than 1 hour, likely continuing
    if gap < timedelta(hours=1):
        return ctx.get('last_topic')
    
    return None


def generate_contextual_greeting(ctx):
    """Generate a contextual greeting based on history."""
    if not ctx.get('last_session_end'):
        return "Hey."
    
    last_end = datetime.fromisoformat(ctx['last_session_end'])
    gap = datetime.now() - last_end
    
    if gap < timedelta(minutes=30):
        return "Back already?"
    elif gap < timedelta(hours=2):
        topic = ctx.get('last_topic', 'that')
        return f"Back to {topic}?"
    elif gap < timedelta(days=1):
        return "Good to see you again."
    elif gap < timedelta(days=7):
        return "Welcome back."
    else:
        return "It's been a while. How have you been?"


def end_session(topic=None, actions_pending=None):
    """Record session end."""
    ctx = load_context()
    
    ctx['last_session_end'] = datetime.now().isoformat()
    
    if topic:
        ctx['last_topic'] = topic
        # Track topic frequency
        if topic not in ctx['topics']:
            ctx['topics'][topic] = {'count': 0, 'last': None}
        ctx['topics'][topic]['count'] += 1
        ctx['topics'][topic]['last'] = datetime.now().isoformat()
    
    if actions_pending:
        ctx['pending_actions'] = actions_pending
    else:
        ctx['pending_actions'] = []
    
    save_context(ctx)


def get_topic_summary(days=7):
    """Get summary of recent topics."""
    ctx = load_context()
    cutoff = datetime.now() - timedelta(days=days)
    
    recent = []
    for topic, data in ctx.get('topics', {}).items():
        if data['last']:
            last_date = datetime.fromisoformat(data['last'])
            if last_date > cutoff:
                recent.append({
                    'topic': topic,
                    'count': data['count'],
                    'last': data['last']
                })
    
    recent.sort(key=lambda x: x['last'], reverse=True)
    return recent[:5]


def main():
    if len(sys.argv) < 2:
        print("Usage: context_bridge.py --start [platform]")
        print("       context_bridge.py --end [topic] [actions]")
        print("       context_bridge.py --summary")
        print("       context_bridge.py --get-last-topic")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == '--start':
        platform = sys.argv[2] if len(sys.argv) > 2 else "webchat"
        result = start_session(platform)
        print(json.dumps(result, indent=2))
    
    elif cmd == '--end':
        topic = sys.argv[2] if len(sys.argv) > 2 else None
        actions = sys.argv[3:] if len(sys.argv) > 3 else None
        end_session(topic, actions)
        print(json.dumps({'status': 'session_ended'}, indent=2))
    
    elif cmd == '--summary':
        summary = get_topic_summary()
        print(json.dumps({
            'recent_topics': summary,
            'total_sessions': len(load_context().get('sessions', []))
        }, indent=2))
    
    elif cmd == '--get-last-topic':
        ctx = load_context()
        print(json.dumps({
            'last_topic': ctx.get('last_topic'),
            'pending_actions': ctx.get('pending_actions', [])
        }, indent=2))
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
