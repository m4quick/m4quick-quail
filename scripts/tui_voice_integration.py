#!/usr/bin/env python3
"""
TUI Voice Integration with Channel Logging
Logs all conversations for cross-instance memory.
"""

import subprocess
import sys
import os

# Add workspace to path for channel_logs
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace"))

from memory.channel_logs import log_message

def main():
    # Log the voice command initiation
    log_message('tui', 'user', '[Voice command initiated]', instance_id='tui-voice-session')
    
    # Clear line for TUI
    print("\r" + " " * 80, end="\r")
    print("🎤 Recording 5 seconds... Speak now!")
    
    # Run voice_mic.py
    result = subprocess.run(
        [sys.executable, os.path.expanduser("~/.openclaw/workspace/scripts/voice_mic.py"), "-d", "5"],
        capture_output=False,
        text=True
    )
    
    # Log completion
    log_message('tui', 'system', '[Voice command completed]', instance_id='tui-voice-session')
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
