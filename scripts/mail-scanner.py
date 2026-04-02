#!/usr/bin/env python3
"""
Mail Scanner - Find sales/advertising emails via AppleScript
Searches by sender patterns and keywords
"""

import subprocess
import sys
import re
from datetime import datetime

def run(script, timeout=30):
    """Execute AppleScript"""
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip() if result.returncode == 0 else None

# Sales/advertising patterns to search for
SALES_PATTERNS = [
    'sale', 'promo', 'deal', 'discount', 'offer', 'save', 'coupon',
    'clearance', 'bogo', 'limited', 'special', 'price drop', '% off',
    'unsubscribe', 'marketing', 'advertising', 'shop now',
    'order confirmation', 'shipping notification', 'tracking number'
]

def get_sample_senders(count=100):
    """Get sample of recent senders to identify patterns"""
    script = f'''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            tell mailbox "Inbox"
                set total to count of messages
                set senders to {{}}
                set step to total div {count}
                if step < 1 then set step to 1
                
                repeat with i from total to 1 by -step
                    if length of senders >= {count} then exit repeat
                    try
                        set s to sender of message i
                        if s is not in senders then set end of senders to s
                    end try
                end repeat
                
                return senders as string
            end tell
        end tell
    end tell
    '''
    return run(script, timeout=60)

def search_by_subject(pattern, max_results=50):
    """Search emails by subject keyword"""
    script = f'''
    tell application "Mail"
        tell account "mmirzaie@msn.com"
            tell mailbox "Inbox"
                set matches to {{}}
                set total to count of messages
                set checked to 0
                
                repeat with i from total to 1 by -1
                    set checked to checked + 1
                    if length of matches >= {max_results} then exit repeat
                    if checked > 5000 then exit repeat  -- Limit search scope
                    
                    try
                        set m to message i
                        set subj to subject of m
                        if "{pattern}" is in subj then
                            set end of matches to {{id:(id of m), subject:subj, sender:(sender of m), date:(date received of m)}}
                        end if
                    end try
                end repeat
                
                set out to ""
                repeat with m in matches
                    set out to out & (id of m) & "|" & (subject of m) & "|" & (sender of m) & "|" & (date received of m) & "\\n"
                end repeat
                return out
            end tell
        end tell
    end tell
    '''
    return run(script, timeout=60)

def analyze_senders(senders_text):
    """Analyze sender list for sales/advertising patterns"""
    if not senders_text:
        return {}
    
    senders = [s.strip() for s in senders_text.split(",") if s.strip()]
    
    categories = {
        'retail': [],
        'newsletters': [],
        'shipping': [],
        'promotions': [],
        'other': []
    }
    
    retail_domains = ['amazon', 'walmart', 'target', 'bestbuy', 'homedepot', 'lowes', 'costco', 'ebay', 'etsy']
    newsletter_keywords = ['newsletter', 'digest', 'weekly', 'daily', 'update']
    shipping_keywords = ['usps', 'ups', 'fedex', 'dhl', 'shipping', 'tracking', 'delivered']
    promo_keywords = ['noreply', 'info', 'marketing', 'promotions', 'deals', 'offers', 'sale']
    
    for sender in senders:
        sender_lower = sender.lower()
        categorized = False
        
        for domain in retail_domains:
            if domain in sender_lower:
                categories['retail'].append(sender)
                categorized = True
                break
        
        if not categorized:
            for kw in shipping_keywords:
                if kw in sender_lower:
                    categories['shipping'].append(sender)
                    categorized = True
                    break
        
        if not categorized:
            for kw in promo_keywords:
                if kw in sender_lower:
                    categories['promotions'].append(sender)
                    categorized = True
                    break
        
        if not categorized:
            for kw in newsletter_keywords:
                if kw in sender_lower:
                    categories['newsletters'].append(sender)
                    categorized = True
                    break
        
        if not categorized:
            categories['other'].append(sender)
    
    return categories

def main():
    print("=" * 70)
    print("MAIL SCANNER - Sales & Advertising Detection")
    print("=" * 70)
    print()
    print("Scanning for sender patterns...")
    print("(This may take 30-60 seconds)")
    print()
    
    # Get sample senders
    senders = get_sample_senders(100)
    if not senders:
        print("Failed to retrieve senders. macOS Mail may need to be running.")
        sys.exit(1)
    
    print(f"✓ Analyzed {len([s for s in senders.split(',') if s.strip()])} unique senders")
    print()
    
    # Categorize
    categories = analyze_senders(senders)
    
    print("SENDER CATEGORIES FOUND:")
    print("-" * 70)
    
    for cat, items in categories.items():
        if items:
            print(f"\n{cat.upper()} ({len(items)} senders):")
            for item in items[:10]:  # Show first 10
                print(f"  • {item}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more")
    
    print()
    print("=" * 70)
    print("SUBJECT KEYWORD SEARCH")
    print("=" * 70)
    
    # Search by key patterns
    for pattern in ['unsubscribe', 'sale', 'order confirmed', 'shipping']:
        print(f"\nSearching for '{pattern}' in subject...")
        results = search_by_subject(pattern, 20)
        if results:
            lines = [l for l in results.strip().split("\\n") if l]
            print(f"  Found {len(lines)} matches")
            for line in lines[:5]:
                parts = line.split("|")
                if len(parts) >= 3:
                    print(f"    - {parts[1][:50]}... ({parts[2][:30]})")
            if len(lines) > 5:
                print(f"    ... and {len(lines) - 5} more")
        else:
            print("  No matches found")
    
    print()
    print("=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    print()
    print("Based on scan results, here are suggested archive targets:")
    print()
    print("1. RETAIL NOTIFICATIONS (Amazon, Walmart, etc.)")
    print("   → Can archive order confirmations older than 1 year")
    print("   → Keep recent shipping notifications (30 days)")
    print()
    print("2. PROMOTIONAL EMAILS (noreply@*, marketing@*)")
    print("   → Safe to archive/delete all promotional emails")
    print("   → Consider unsubscribing from dead lists")
    print()
    print("3. SHIPPING NOTIFICATIONS (USPS, UPS, FedEx)")
    print("   → Archive delivered items older than 30 days")
    print("   → Keep in-transit notifications")
    print()
    print("4. NEWSLETTERS")
    print("   → Archive all if not reading regularly")
    print("   → Or create 'Newsletters' folder")
    print()
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print("Option A: Generate specific archive script")
    print("  - Target specific senders/domains")
    print("  - Preview before moving")
    print()
    print("Option B: Create smart folders in macOS Mail")
    print("  - Auto-sort future incoming mail")
    print()
    print("Option C: Bulk archive by date")
    print("  - Archive pre-2023 emails to Archive folder")
    print()
    print("Choose A, B, or C (or specify a sender/domain to target)")

if __name__ == '__main__':
    main()
