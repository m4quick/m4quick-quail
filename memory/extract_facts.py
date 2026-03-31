#!/usr/bin/env python3
"""
Memory Fact Extractor - Phase 1.2
Automatically extracts facts from conversations and saves for review.

Usage:
    python3 memory/extract_facts.py "conversation text here"
    
Or from file:
    python3 memory/extract_facts.py --file conversation.txt
"""

import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
EXTRACTED_DIR = MEMORY_DIR / "auto-extracted"
PENDING_FILE = EXTRACTED_DIR / "pending_facts.json"

# Patterns that indicate facts worth extracting
FACT_PATTERNS = [
    # Preferences
    (r'(?:I prefer|preferred|like|dislike|hate|love|enjoy)\s+(?:to\s+)?(.+?)[.!;]', 'preference'),
    (r'(?:my favorite|my least favorite)\s+(?:is|are)\s+(.+?)[.!;]', 'preference'),
    
    # Decisions
    (r"(?:let's|we should|decided to|going to|plan to)\s+(.+?)[.!;]", 'decision'),
    (r'(?:agreed on|settled on|chose|picked)\s+(.+?)[.!;]', 'decision'),
    
    # Facts about user
    (r"(?:I am|I work as|my job is|I'm)\s+(?:a\s+)?(.+?)[.!;]", 'identity'),
    (r'(?:I have|I own|I use)\s+(.+?)[.!;]', 'possession'),
    
    # Important info
    (r"(?:remember that|don't forget|important|note that)\s+(.+?)[.!;]", 'important'),
    
    # Schedule/Time
    (r'(?:every|each|daily|weekly|monthly)\s+(.+?)(?:at|on)\s+(.+?)[.!;]', 'schedule'),
    (r'(?:scheduled|set for|due on)\s+(.+?)[.!;]', 'schedule'),
]

# Things to explicitly NOT extract (privacy/safety)
EXCLUDE_PATTERNS = [
    r'\b\d{3}-\d{2}-\d{4}\b',  # SSN-like
    r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
    r'password[=:]\s*\S+',  # password=xxx
    r'api[_-]?key[=:]\s*\S+',  # api_key=xxx
]


def sanitize(text):
    """Remove potentially sensitive info."""
    for pattern in EXCLUDE_PATTERNS:
        text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)
    return text


def extract_facts(text):
    """Extract potential facts from text."""
    facts = []
    text = sanitize(text)
    
    for pattern, category in FACT_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            fact_text = match.group(1).strip()
            if len(fact_text) > 10:  # Ignore very short matches
                facts.append({
                    'text': fact_text,
                    'category': category,
                    'full_context': match.group(0),
                    'extracted_at': datetime.now().isoformat(),
                    'approved': None  # None = pending, True = approved, False = rejected
                })
    
    return facts


def load_pending():
    """Load existing pending facts."""
    if PENDING_FILE.exists():
        with open(PENDING_FILE) as f:
            return json.load(f)
    return {'facts': [], 'last_reviewed': None}


def save_pending(data):
    """Save pending facts."""
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    with open(PENDING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_facts.py 'conversation text'")
        print("       extract_facts.py --file conversation.txt")
        sys.exit(1)
    
    # Get input text
    if sys.argv[1] == '--file':
        with open(sys.argv[2]) as f:
            text = f.read()
    else:
        text = ' '.join(sys.argv[1:])
    
    # Extract facts
    new_facts = extract_facts(text)
    
    if not new_facts:
        print("No facts extracted.")
        return
    
    # Load existing and merge
    data = load_pending()
    existing_texts = {f['text'] for f in data['facts']}
    
    added = 0
    for fact in new_facts:
        if fact['text'] not in existing_texts:
            data['facts'].append(fact)
            added += 1
    
    # Save
    save_pending(data)
    
    print(f"Extracted {added} new fact(s). Total pending: {len(data['facts'])}")
    for f in new_facts[:3]:  # Show first 3
        print(f"  [{f['category']}] {f['text'][:60]}...")


if __name__ == '__main__':
    main()
