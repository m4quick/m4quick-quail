#!/bin/bash
# Inanna initialization script - SQLite shared memory

DB_FILE="$HOME/.openclaw/workspace/memory/conversation.db"

# Read existing messages on startup
if [ -f "$DB_FILE" ]; then
    echo "=== Recent messages ==="
    sqlite3 "$DB_FILE" "SELECT timestamp, message FROM messages ORDER BY id DESC LIMIT 10;"
    echo ""
fi

# Function to log messages (safe quoting)
log_message() {
    local msg="$1"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Use single quotes around SQL, escape single quotes in message
    local escaped_msg=$(echo "$msg" | sed "s/'/''/g")
    
    sqlite3 "$DB_FILE" "INSERT INTO messages (timestamp, message) VALUES ('$timestamp', '$escaped_msg');"
}

# Log startup
log_message "Inanna initialized and ready."

echo "Inanna online. Database: $DB_FILE"
