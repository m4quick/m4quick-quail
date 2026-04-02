#!/usr/bin/env python3
"""
Mail Bridge - macOS Mail CLI wrapper
Optimized for large mailboxes - uses direct index access
"""

import subprocess
import sys
import json
import argparse

def run(script, timeout=10):
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip() if result.returncode == 0 else None

def cmd_count(args):
    """Count messages in folder"""
    script = f'tell application "Mail" to return (count of messages in mailbox "{args.folder}" of account "mmirzaie@msn.com") as string'
    result = run(script, timeout=5)
    count = int(result) if result and result.isdigit() else 0
    print(json.dumps({"folder": args.folder, "count": count}) if args.json else f"{args.folder}: {count} messages")

def cmd_folders(args):
    """List mailboxes"""
    script = '''tell application "Mail"
        set acc to account "mmirzaie@msn.com"
        set names to {}
        repeat with mb in mailboxes of acc
            set end of names to name of mb
        end repeat
        return names as string
    end tell'''
    result = run(script, timeout=10)
    folders = [x.strip() for x in result.split(",")] if result else []
    if args.json:
        print(json.dumps({"folders": folders}))
    else:
        print("\\n".join(folders))

def cmd_list(args):
    """List recent messages - optimized"""
    # Get count
    count_script = f'tell application "Mail" to return (count of messages in mailbox "{args.folder}" of account "mmirzaie@msn.com") as string'
    count_result = run(count_script, timeout=5)
    total = int(count_result) if count_result and count_result.isdigit() else 0
    
    if total == 0:
        print("No messages")
        return
    
    # Fetch last N messages by index (newest first)
    start_idx = max(1, total - args.limit + 1)
    messages = []
    
    print(f"Fetching {args.limit} most recent from {total} total...", file=sys.stderr)
    
    for idx in range(total, start_idx - 1, -1):
        script = f'''
        tell application "Mail"
            tell account "mmirzaie@msn.com"
                tell mailbox "{args.folder}"
                    set m to message {idx}
                    return (id of m) & "|" & (subject of m) & "|" & (sender of m) & "|" & (date received of m) & "|" & (read status of m)
                end tell
            end tell
        end tell'''
        result = run(script, timeout=5)
        if result and "|" in result:
            parts = result.split("|")
            if len(parts) >= 5:
                messages.append({
                    "id": parts[0],
                    "subject": parts[1] if parts[1] else "(no subject)",
                    "from": parts[2] if parts[2] else "(unknown)",
                    "date": parts[3],
                    "read": parts[4] == "true"
                })
    
    if args.json:
        print(json.dumps(messages))
    else:
        print(f"{'ID':<10} {'✓':<3} {'From':<35} {'Subject'}")
        print("-" * 85)
        for m in messages:
            read = "✓" if m['read'] else " "
            from_short = m['from'][:33] + "..." if len(m['from']) > 35 else m['from']
            subj = m['subject'][:45] + "..." if len(m['subject']) > 45 else m['subject']
            print(f"{m['id']:<10} {read:<3} {from_short:<35} {subj}")

def cmd_read(args):
    """Read a specific message"""
    if not args.id:
        print("Error: Message ID required")
        sys.exit(1)
    
    script = f'''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            set m to first message whose id is {args.id}
            set content_text to content of m
            return "From: " & (sender of m) & "\\nSubject: " & (subject of m) & "\\nDate: " & (date received of m) & "\\n\\n" & content_text
        end tell
    end tell'''
    result = run(script, timeout=10)
    if result:
        print(result)
    else:
        print(f"Message {args.id} not found")

def cmd_send(args):
    """Send a message"""
    if not args.to or not args.subject:
        print("Error: --to and --subject required")
        sys.exit(1)
    
    body = sys.stdin.read() if not sys.stdin.isatty() else input("Body (Ctrl+D to finish):\\n")
    
    # Escape for AppleScript
    subj = args.subject.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
    body = body.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
    
    script = f'''
    tell application "Mail"
        set m to make new outgoing message with properties {{subject:"{subj}", content:"{body}"}}
        tell m
            make new to recipient with properties {{address:"{args.to}"}}
        end tell
        send m
        return "Sent"
    end tell'''
    result = run(script, timeout=30)
    print(result if result else "Failed")

def main():
    parser = argparse.ArgumentParser(description='Mail Bridge - macOS Mail CLI')
    subparsers = parser.add_subparsers(dest='cmd')
    
    # count
    p_count = subparsers.add_parser('count', help='Count messages')
    p_count.add_argument('--folder', default='Inbox')
    p_count.add_argument('--json', action='store_true')
    
    # folders
    p_folders = subparsers.add_parser('folders', help='List folders')
    p_folders.add_argument('--json', action='store_true')
    
    # list
    p_list = subparsers.add_parser('list', help='List messages')
    p_list.add_argument('--folder', default='Inbox')
    p_list.add_argument('-n', '--limit', type=int, default=10)
    p_list.add_argument('--json', action='store_true')
    
    # read
    p_read = subparsers.add_parser('read', help='Read message')
    p_read.add_argument('--id', required=True)
    
    # send
    p_send = subparsers.add_parser('send', help='Send message')
    p_send.add_argument('--to', required=True)
    p_send.add_argument('--subject', required=True)
    
    args = parser.parse_args()
    
    if args.cmd == 'count':
        cmd_count(args)
    elif args.cmd == 'folders':
        cmd_folders(args)
    elif args.cmd == 'list':
        cmd_list(args)
    elif args.cmd == 'read':
        cmd_read(args)
    elif args.cmd == 'send':
        cmd_send(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
