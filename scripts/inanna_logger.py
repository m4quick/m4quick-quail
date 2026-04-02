#!/usr/bin/env python3
"""
Secure SQLite logger for Inanna
Avoids SQL injection via parameterized queries
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".openclaw" / "workspace" / "memory" / "shared_conversation.db"

def init_db():
    """Initialize database with schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            instance TEXT NOT NULL,
            speaker TEXT NOT NULL,
            msg TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_time ON messages(time)
    ''')
    
    conn.commit()
    conn.close()

def log_message(speaker: str, msg: str, instance: str = "inanna"):
    """Log message securely with parameterized query."""
    init_db()
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # SAFE: Parameterized query prevents SQL injection
    cursor.execute('''
        INSERT INTO messages (time, instance, speaker, msg)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().isoformat(), instance, speaker, msg))
    
    conn.commit()
    conn.close()

def get_recent_messages(hours: int = 24, limit: int = 50):
    """Get recent messages for context."""
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT time, instance, speaker, msg
        FROM messages
        WHERE time > datetime('now', '-' || ? || ' hours')
        ORDER BY time DESC
        LIMIT ?
    ''', (hours, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1:
        msg = ' '.join(sys.argv[1:])
        log_message('inanna', msg)
        print(f"Logged: {msg}")
    else:
        # Show recent
        print("Recent messages:")
        for row in get_recent_messages():
            print(f"[{row[0]}] {row[2]}: {row[3][:60]}...")
