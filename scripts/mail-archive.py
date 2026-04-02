#!/usr/bin/env python3
"""
Mail Archive Tool - Sales & Advertising Cleanup
Uses macOS Mail via AppleScript - works with any configured account
"""

import subprocess
import sys
import argparse
from datetime import datetime

# Sales/advertising sender patterns to archive
TARGET_SENDERS = [
    # AliExpress promotional
    "promotion@aliexpress.com",
    "ae-news-interest03@mail.aliexpress.com", 
    "ae.like05@mail.aliexpress.com",
    "info-buyer01.g@mail.aliexpress.com",
    "buyer-info3.g@mail.aliexpress.com",
    "ae-news-interest03@mail.aliexpress.com",
    
    # Amazon marketing
    "aws-marketing-email-replies@amazon.com",
    "vfe-campaign-response@amazon.com",
    
    # Newsletters
    "newsletters@cnet.online.com",
    "mail@mail.adobe.com",
]

def run(script, timeout=60):
    """Execute AppleScript"""
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip() if result.returncode == 0 else None

def ensure_archive_folder():
    """Create Archive/Sales-Ads folder if it doesn't exist"""
    script = '''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            try
                set archiveFolder to mailbox "Archive"
            on error
                set archiveFolder to make new mailbox with properties {name:"Archive"}
            end try
            
            try
                set salesFolder to mailbox "Sales-Ads" of archiveFolder
            on error
                set salesFolder to make new mailbox at archiveFolder with properties {name:"Sales-Ads"}
            end try
            
            return "Archive/Sales-Ads ready"
        end tell
    end tell
    '''
    return run(script, timeout=10)

def find_messages_by_sender(sender_email, max_check=5000):
    """Find messages from a specific sender"""
    script = f'''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            tell mailbox "Inbox"
                set matches to {{}}
                set total to count of messages
                set checked to 0
                
                repeat with i from total to 1 by -1
                    set checked to checked + 1
                    if checked > {max_check} then exit repeat
                    
                    try
                        set m to message i
                        set msgSender to sender of m
                        if "{sender_email}" is in msgSender then
                            set end of matches to {{id:(id of m), subject:(subject of m), date:(date received of m)}}
                        end if
                    end try
                end repeat
                
                set out to ""
                repeat with m in matches
                    set out to out & (id of m) & "|" & (subject of m) & "|" & (date received of m) & "\\n"
                end repeat
                return out & "COUNT:" & (count of matches)
            end tell
        end tell
    end tell
    '''
    return run(script, timeout=120)

def move_messages_to_archive(message_ids):
    """Move messages to Archive/Sales-Ads"""
    script = f'''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            set targetFolder to mailbox "Sales-Ads" of mailbox "Archive"
            set movedCount to 0
            
            repeat with msgId in {{{','.join(message_ids)}}}
                try
                    set m to first message whose id is msgId
                    move m to targetFolder
                    set movedCount to movedCount + 1
                end try
            end repeat
            
            return "Moved " & movedCount & " messages"
        end tell
    end tell
    '''
    return run(script, timeout=60)

def preview_sender(sender_email):
    """Show preview of what would be archived"""
    print(f"\\nScanning for: {sender_email}")
    print("-" * 60)
    
    result = find_messages_by_sender(sender_email, max_check=2000)
    if not result:
        print("  No matches found (or timeout)")
        return []
    
    lines = result.strip().split("\\n")
    messages = []
    total_count = 0
    
    for line in lines:
        if line.startswith("COUNT:"):
            total_count = int(line.replace("COUNT:", ""))
        elif "|" in line:
            parts = line.split("|")
            if len(parts) >= 3:
                messages.append({
                    "id": parts[0],
                    "subject": parts[1] if parts[1] else "(no subject)",
                    "date": parts[2]
                })
    
    print(f"  Found: {total_count} messages")
    
    # Show sample
    for msg in messages[:5]:
        subject_short = msg['subject'][:50] + "..." if len(msg['subject']) > 50 else msg['subject']
        print(f"    - {subject_short}")
    
    if total_count > 5:
        print(f"    ... and {total_count - 5} more")
    
    return messages

def main():
    parser = argparse.ArgumentParser(description='Mail Archive Tool - Sales/Advertising cleanup')
    parser.add_argument('--dry-run', action='store_true', help='Preview only, do not move')
    parser.add_argument('--sender', help='Target specific sender (default: all sales/ads)')
    parser.add_argument('--batch-size', type=int, default=50, help='Messages to move per batch')
    args = parser.parse_args()
    
    print("=" * 70)
    print("MAIL ARCHIVE TOOL - Sales/Advertising Cleanup")
    print("=" * 70)
    print()
    
    # Ensure folder exists
    print("Setting up Archive/Sales-Ads folder...")
    result = ensure_archive_folder()
    print(f"  {result}")
    print()
    
    # Determine targets
    if args.sender:
        targets = [args.sender]
    else:
        targets = TARGET_SENDERS
    
    # Preview phase
    all_matches = []
    for sender in targets:
        matches = preview_sender(sender)
        all_matches.extend(matches)
    
    if args.dry_run:
        print()
        print("=" * 70)
        print("DRY RUN - No messages were moved")
        print(f"Total that would be archived: {len(all_matches)}")
        print("=" * 70)
        return
    
    if not all_matches:
        print("\\nNo messages found to archive.")
        return
    
    # Confirm
    print()
    print("=" * 70)
    print(f"Ready to archive {len(all_matches)} messages")
    print("=" * 70)
    print()
    
    response = input("Proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Move in batches
    print("\\nArchiving messages...")
    batch_size = args.batch_size
    total_moved = 0
    
    for i in range(0, len(all_matches), batch_size):
        batch = all_matches[i:i+batch_size]
        ids = [m['id'] for m in batch]
        
        result = move_messages_to_archive(ids)
        if result:
            print(f"  {result}")
            total_moved += len(batch)
        else:
            print(f"  Failed to move batch {i//batch_size + 1}")
    
    print()
    print("=" * 70)
    print(f"COMPLETE - Archived {total_moved} messages")
    print("=" * 70)

if __name__ == '__main__':
    main()
