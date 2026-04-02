#!/usr/bin/env python3
"""
Mail Archive Tool - AliExpress Test
Focused on AliExpress promotional emails only
"""

import subprocess
import sys

def run(script, timeout=120):
    """Execute AppleScript"""
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip() if result.returncode == 0 else None

def setup_folders():
    """Create Archive/Sales-Ads folder structure"""
    script = '''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            -- Create Archive if needed
            try
                set archiveBox to mailbox "Archive"
            on error
                set archiveBox to make new mailbox with properties {name:"Archive"}
            end try
            
            -- Create Sales-Ads subfolder
            try
                set salesBox to mailbox "Sales-Ads" of archiveBox
                return "Folders ready"
            on error
                set salesBox to make new mailbox at archiveBox with properties {name:"Sales-Ads"}
                return "Created Archive/Sales-Ads"
            end try
        end tell
    end tell
    '''
    return run(script, timeout=10)

def find_aliexpress_sample():
    """Find sample of AliExpress emails (search last 1000 messages)"""
    script = '''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            tell mailbox "Inbox"
                set total to count of messages
                set matches to {}
                set searchLimit to 1000
                
                if total < searchLimit then set searchLimit to total
                
                set startIdx to total - searchLimit + 1
                if startIdx < 1 then set startIdx to 1
                
                repeat with i from total to startIdx by -1
                    try
                        set m to message i
                        set msgSender to sender of m
                        set msgSubject to subject of m
                        
                        -- Check for AliExpress patterns
                        if ("aliexpress" is in msgSender) or ("aliexpress" is in msgSubject) then
                            set end of matches to {id:(id of m), subject:msgSubject, sender:msgSender, idx:i}
                        end if
                    end try
                end repeat
                
                -- Build output
                set out to ""
                repeat with m in matches
                    set out to out & (id of m) & "||" & (subject of m) & "||" & (sender of m) & "||" & (idx of m) & "\\n"
                end repeat
                
                return out & "TOTAL:" & (count of matches)
            end tell
        end tell
    end tell
    '''
    return run(script, timeout=90)

def move_messages(msg_ids):
    """Move specific messages to Archive/Sales-Ads"""
    ids_str = ",".join(msg_ids)
    script = f'''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            set targetFolder to mailbox "Sales-Ads" of mailbox "Archive"
            set movedCount to 0
            set failedCount to 0
            
            set idList to {{{ids_str}}}
            repeat with msgId in idList
                try
                    set m to first message whose id is msgId
                    move m to targetFolder
                    set movedCount to movedCount + 1
                on error
                    set failedCount to failedCount + 1
                end try
            end repeat
            
            return "Moved: " & movedCount & ", Failed: " & failedCount
        end tell
    end tell
    '''
    return run(script, timeout=60)

def main():
    print("=" * 70)
    print("ALIEXPRESS ARCHIVE TEST")
    print("=" * 70)
    print()
    
    # Setup folders
    print("Setting up folder structure...")
    result = setup_folders()
    print(f"  {result}")
    print()
    
    # Find AliExpress emails
    print("Scanning last 1000 messages for AliExpress...")
    print("(This may take 30-60 seconds)")
    print()
    
    result = find_aliexpress_sample()
    if not result:
        print("No AliExpress emails found in recent messages.")
        return
    
    # Parse results
    lines = result.strip().split("\\n")
    messages = []
    total_count = 0
    
    for line in lines:
        if line.startswith("TOTAL:"):
            total_count = int(line.replace("TOTAL:", ""))
        elif "||" in line:
            parts = line.split("||")
            if len(parts) >= 3:
                messages.append({
                    "id": parts[0],
                    "subject": parts[1],
                    "sender": parts[2]
                })
    
    print(f"Found {total_count} AliExpress messages")
    print()
    
    if total_count == 0:
        print("No AliExpress emails to archive.")
        return
    
    # Show preview
    print("Sample of what would be archived:")
    print("-" * 70)
    for msg in messages[:10]:
        subject = msg['subject'][:55] + "..." if len(msg['subject']) > 55 else msg['subject']
        sender = msg['sender'][:35] + "..." if len(msg['sender']) > 35 else msg['sender']
        print(f"  ID {msg['id']:<8} | {sender:<40} | {subject}")
    
    if total_count > 10:
        print(f"  ... and {total_count - 10} more")
    
    print()
    print("-" * 70)
    print()
    
    # Confirm
    print(f"Ready to move {total_count} AliExpress messages to Archive/Sales-Ads")
    print()
    response = input("Type 'move' to proceed, 'preview' to see more samples, or anything else to cancel: ")
    
    if response.lower() == 'move':
        print()
        print("Moving messages...")
        ids = [m['id'] for m in messages]
        result = move_messages(ids)
        print(f"  {result}")
        print()
        print("=" * 70)
        print("Done! Check Archive/Sales-Ads in Mail.app")
        print("=" * 70)
    elif response.lower() == 'preview':
        print()
        print("Showing all matches:")
        for msg in messages:
            print(f"  {msg['sender']:<40} | {msg['subject'][:50]}")
    else:
        print()
        print("Cancelled. No messages were moved.")

if __name__ == '__main__':
    main()
