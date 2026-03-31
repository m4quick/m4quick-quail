#!/usr/bin/env python3
"""
Natural Language System Query - Phase 1.3
Ask about your system in plain English.

Usage:
    python3 scripts/system_query.py "How's my disk?"
    python3 scripts/system_query.py "Why is my system slow?"
    python3 scripts/system_query.py "Check Pi-hole status"
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "heartbeat-state.json"

# Intent patterns
INTENTS = {
    'disk_status': [
        r'how.*disk',
        r'disk.*usage',
        r'storage.*space',
        r'free.*space',
        r'disk.*full',
    ],
    'memory_status': [
        r'how.*memory',
        r'memory.*usage',
        r'ram.*usage',
        r'system.*slow',
        r'running.*slow',
    ],
    'pihole_status': [
        r'pihole',
        r'pi-hole',
        r'dns.*status',
        r'network.*status',
    ],
    'n8n_status': [
        r'n8n',
        r'automation.*status',
    ],
    'overall_status': [
        r'how.*system',
        r'system.*status',
        r'everything.*ok',
        r'any.*issues',
        r'check.*system',
    ],
    'daily_report': [
        r'daily.*report',
        r'status.*report',
        r'what.*happened.*today',
    ],
}


def detect_intent(query):
    """Detect what the user is asking about."""
    query_lower = query.lower()
    
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if re.search(pattern, query_lower):
                return intent
    
    return 'unknown'


def run_command(cmd):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def get_disk_info():
    """Get disk usage info."""
    df_output = run_command("df -h ~ | tail -1")
    usage_percent = int(run_command("df ~ | tail -1 | awk '{print $5}' | tr -d '%'"))
    
    status = "✅ Good"
    if usage_percent > 90:
        status = "🚨 CRITICAL"
    elif usage_percent > 80:
        status = "⚠️ Warning"
    
    return {
        'raw': df_output,
        'percent': usage_percent,
        'status': status,
        'message': f"{status} — Disk is {usage_percent}% full."
    }


def get_memory_info():
    """Get memory pressure info."""
    pressure_output = run_command("memory_pressure 2>/dev/null | grep 'free percentage' | awk '{print $NF}' | tr -d '%'")
    
    try:
        free_percent = int(pressure_output) if pressure_output else 0
    except:
        free_percent = 0
    
    status = "✅ Good"
    if free_percent < 20:
        status = "🚨 CRITICAL"
    elif free_percent < 50:
        status = "⚠️ Warning"
    
    return {
        'free_percent': free_percent,
        'status': status,
        'message': f"{status} — {free_percent}% memory free."
    }


def get_pihole_info():
    """Get Pi-hole status."""
    container_status = run_command("ssh -o ConnectTimeout=5 pi@192.168.1.57 'sudo docker inspect --format=\"{{.State.Status}}\" pihole 2>/dev/null' || echo 'unreachable'")
    
    if container_status == "running":
        return {
            'status': "✅ Running",
            'message': "Pi-hole container is running and healthy."
        }
    elif container_status == "unreachable":
        return {
            'status': "⚠️ Unreachable",
            'message': "Cannot reach Pi-hole host (192.168.1.57). Check network."
        }
    else:
        return {
            'status': "🚨 Down",
            'message': f"Pi-hole container is {container_status}. SSH and restart if needed."
        }


def get_n8n_info():
    """Get n8n status."""
    status = run_command("docker inspect --format='{{.State.Status}}' n8n 2>/dev/null || echo 'not_running'")
    
    if status == "running":
        return {
            'status': "✅ Running",
            'message': "n8n automation platform is running."
        }
    else:
        return {
            'status': "🚨 Down",
            'message': f"n8n is {status}. Run: docker start n8n"
        }


def get_overall_status():
    """Get comprehensive system status."""
    results = []
    issues = []
    
    # Disk
    disk = get_disk_info()
    results.append(f"💾 Disk: {disk['message']}")
    if "🚨" in disk['status'] or "⚠️" in disk['status']:
        issues.append("Disk space")
    
    # Memory
    mem = get_memory_info()
    results.append(f"🧠 Memory: {mem['message']}")
    if "🚨" in mem['status'] or "⚠️" in mem['status']:
        issues.append("Memory pressure")
    
    # Pi-hole
    pihole = get_pihole_info()
    results.append(f"🌐 Pi-hole: {pihole['message']}")
    if "🚨" in pihole['status']:
        issues.append("Pi-hole")
    
    # n8n
    n8n = get_n8n_info()
    results.append(f"⚙️ n8n: {n8n['message']}")
    if "🚨" in n8n['status']:
        issues.append("n8n")
    
    # Summary
    if issues:
        summary = f"\n⚠️ **Attention needed:** {', '.join(issues)}"
    else:
        summary = "\n✅ **All systems operational**"
    
    return '\n'.join(results) + summary


def answer_disk_query():
    """Answer disk-related queries."""
    info = get_disk_info()
    
    if info['percent'] > 90:
        return f"{info['message']}\n\nYou should free up space immediately. Large directories:\n" + run_command("du -sh ~/*/ 2>/dev/null | sort -hr | head -5")
    elif info['percent'] > 80:
        return f"{info['message']}\n\nConsider cleaning up soon. Run `df -h ~` for details."
    else:
        return f"{info['message']}\n\nPlenty of space available."


def answer_memory_query():
    """Answer memory-related queries."""
    info = get_memory_info()
    
    if info['free_percent'] < 50:
        top_memory = run_command("ps aux | head -1; ps aux | sort -nk +4 | tail -5")
        return f"{info['message']}\n\nTop memory consumers:\n```\n{top_memory}\n```"
    else:
        return f"{info['message']}\n\nSystem has plenty of memory available."


def answer_daily_report():
    """Answer daily report query."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)
        last_report = state.get('lastDailyReport')
        if last_report:
            dt = datetime.fromtimestamp(last_report)
            return f"Last daily report sent: {dt.strftime('%Y-%m-%d %H:%M')}\n\nThe report runs automatically at 8 AM daily. Check your email (mmirzaie@msn.com)."
    
    return "Daily reports run at 8 AM ET. Today's report should arrive soon if not already sent."


def process_query(query):
    """Process a natural language query."""
    intent = detect_intent(query)
    
    responses = {
        'disk_status': answer_disk_query,
        'memory_status': answer_memory_query,
        'pihole_status': lambda: get_pihole_info()['message'],
        'n8n_status': lambda: get_n8n_info()['message'],
        'overall_status': get_overall_status,
        'daily_report': answer_daily_report,
        'unknown': lambda: "I can check:\n• Disk space\n• Memory usage\n• Pi-hole status\n• n8n status\n• Overall system status\n\nTry: 'How's my disk?' or 'Check system status'"
    }
    
    return responses.get(intent, responses['unknown'])()


def main():
    if len(sys.argv) < 2:
        print("Usage: system_query.py 'your question here'")
        print("\nExamples:")
        print("  'How\\'s my disk?'")
        print("  'Why is my system slow?'")
        print("  'Check Pi-hole status'")
        print("  'Everything ok?'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    response = process_query(query)
    print(response)


if __name__ == '__main__':
    main()
