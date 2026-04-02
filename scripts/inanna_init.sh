#!/bin/bash
# Inanna's initialization script - Fixed version

LOG_FILE="$HOME/.openclaw/workspace/memory/shared_conversation.jsonl"

# Create directory if needed
mkdir -p "$(dirname "$LOG_FILE")"

# Read existing log on startup
if [ -f "$LOG_FILE" ]; then
    echo "=== Last 10 messages ==="
    tail -10 "$LOG_FILE"
    echo ""
fi

# Function to log messages (JSON-safe)
log_message() {
    local message="$1"
    # Escape quotes in message
    local escaped_message=$(echo "$message" | sed 's/"/\\"/g')
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Append to log
    echo "{\"time\": \"$timestamp\", \"instance\": \"inanna\", \"speaker\": \"inanna\", \"msg\": \"$escaped_message\"}" >> "$LOG_FILE"
}

# Log startup message
log_message "Inanna initialized and ready for communication."

echo "Inanna is online. Logging to shared_conversation.jsonl"
