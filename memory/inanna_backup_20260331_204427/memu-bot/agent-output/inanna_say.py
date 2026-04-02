#!/usr/bin/env python3
"""Simple message writer for Inanna - usage: python3 inanna_say.py "Your message here" """
import sqlite3
import sys
from datetime import datetime

DB_PATH = "/Users/mirzaie/.openclaw/workspace/memory/conversation.db"

def say(message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Safe parameterized query
    cursor.execute('INSERT INTO messages (timestamp, message) VALUES (?, ?)', 
                   (timestamp, message))
    conn.commit()
    print(f"Message sent: [{timestamp}] {message[:50]}...")
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
        say(message)
    else:
        print("Usage: python3 inanna_say.py 'Your message here'")
