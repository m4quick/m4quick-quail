#!/bin/bash
# TUI Voice Shortcut - Run this from any terminal to record voice and get response

SCRIPT_DIR="$HOME/.openclaw/workspace/scripts"

echo "🎤 OpenClaw Voice Mode"
echo "====================="
echo ""

# Check if we're in a tmux/screen session (TUI context)
if [ -n "$TMUX" ] || [ -n "$STY" ]; then
    echo "Recording from TUI..."
else
    echo "Recording..."
fi

# Run voice capture
python3 "$SCRIPT_DIR/voice_mic.py" -d 5

echo ""
echo "Done. Press any key to continue..."
read -n 1