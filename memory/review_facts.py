#!/usr/bin/env python3
"""
Memory Fact Review - Weekly Review Interface
Run during the Sunday 1 PM review session.

Usage:
    python3 memory/review_facts.py
    python3 memory/review_facts.py --auto-approve  # Approve all pending
    python3 memory/review_facts.py --reject-all    # Reject all pending
"""

import json
import sys
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
PENDING_FILE = MEMORY_DIR / "auto-extracted" / "pending_facts.json"
APPROVED_FILE = MEMORY_DIR / "auto-extracted" / "approved_facts.json"


def load_json(path, default=None):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default or {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def review_interactive():
    """Interactive review of pending facts."""
    data = load_json(PENDING_FILE, {'facts': []})
    pending = [f for f in data['facts'] if f['approved'] is None]
    
    if not pending:
        print("🎉 No pending facts to review!")
        return
    
    print(f"\n🧠 Memory Review: {len(pending)} fact(s) pending\n")
    print("Commands: [y] approve, [n] reject, [s] skip, [q] quit\n")
    
    approved = []
    rejected = []
    
    for i, fact in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}] Category: {fact['category']}")
        print(f"   Text: {fact['text']}")
        print(f"   Context: {fact['full_context'][:80]}...")
        
        while True:
            choice = input("   → Approve? [y/n/s/q]: ").strip().lower()
            if choice == 'y':
                fact['approved'] = True
                fact['reviewed_at'] = datetime.now().isoformat()
                approved.append(fact)
                break
            elif choice == 'n':
                fact['approved'] = False
                fact['reviewed_at'] = datetime.now().isoformat()
                rejected.append(fact)
                break
            elif choice == 's':
                break
            elif choice == 'q':
                save_results(data, approved, rejected)
                print("\nReview saved. Exiting.")
                return
    
    save_results(data, approved, rejected)
    print(f"\n✅ Review complete: {len(approved)} approved, {len(rejected)} rejected")


def save_results(data, approved, rejected):
    """Save review results."""
    # Update pending file (remove approved/rejected)
    data['facts'] = [f for f in data['facts'] if f['approved'] is None]
    data['last_reviewed'] = datetime.now().isoformat()
    save_json(PENDING_FILE, data)
    
    # Append to approved facts
    if approved:
        approved_data = load_json(APPROVED_FILE, {'facts': []})
        approved_data['facts'].extend(approved)
        save_json(APPROVED_FILE, approved_data)
        
        # Also update MEMORY.md
        update_memory_md(approved)


def update_memory_md(facts):
    """Append approved facts to MEMORY.md."""
    memory_path = MEMORY_DIR / "MEMORY.md"
    
    # Build entry
    lines = ["\n## Auto-Extracted Facts (Approved)\n"]
    lines.append(f"*Reviewed: {datetime.now().strftime("%Y-%m-%d %H:%M")}*\n")
    
    for f in facts:
        lines.append(f"- **[{f['category']}]** {f['text']}")
    
    lines.append("")
    
    # Append to file
    with open(memory_path, 'a') as f:
        f.write('\n'.join(lines))
    
    print(f"   📝 Appended {len(facts)} fact(s) to MEMORY.md")


def auto_approve():
    """Auto-approve all pending facts."""
    data = load_json(PENDING_FILE, {'facts': []})
    pending = [f for f in data['facts'] if f['approved'] is None]
    
    if not pending:
        print("No pending facts.")
        return
    
    for f in pending:
        f['approved'] = True
        f['reviewed_at'] = datetime.now().isoformat()
    
    save_results(data, pending, [])
    print(f"✅ Auto-approved {len(pending)} fact(s)")


def show_stats():
    """Show memory stats."""
    pending = load_json(PENDING_FILE, {'facts': []})
    approved = load_json(APPROVED_FILE, {'facts': []})
    
    pending_count = len([f for f in pending['facts'] if f['approved'] is None])
    approved_count = len(approved.get('facts', []))
    
    print(f"\n🧠 Memory Stats:")
    print(f"   Pending review: {pending_count}")
    print(f"   Approved: {approved_count}")
    print(f"   Last reviewed: {pending.get('last_reviewed', 'Never')}")


if __name__ == '__main__':
    if '--stats' in sys.argv:
        show_stats()
    elif '--auto-approve' in sys.argv:
        auto_approve()
    elif '--reject-all' in sys.argv:
        data = load_json(PENDING_FILE, {'facts': []})
        for f in data['facts']:
            f['approved'] = False
        data['facts'] = []
        save_json(PENDING_FILE, data)
        print("Rejected all pending facts.")
    else:
        review_interactive()
