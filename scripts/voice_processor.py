#!/usr/bin/env python3
"""
Voice Processor - Phase 2.1
Process voice notes from Telegram/WhatsApp
Convert speech to intent, generate voice + text response

Usage:
    python3 scripts/voice_processor.py /path/to/audio.ogg "transcribed text"
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"


def text_to_speech(text, output_path=None):
    """Generate voice response using macOS say command."""
    if output_path:
        # Save to file
        cmd = ['say', '-v', 'Daniel', '-o', str(output_path), text]
    else:
        # Play immediately
        cmd = ['say', '-v', 'Daniel', text]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        return False


def process_voice_command(transcribed_text, audio_path=None):
    """Process transcribed voice command."""
    
    # Import system query logic
    sys.path.insert(0, str(WORKSPACE / "scripts"))
    from system_query import process_query, detect_intent
    
    # Clean up transcription (remove filler words, normalize)
    text = transcribed_text.lower().strip()
    text = text.replace("hey enki", "").replace("okay enki", "").strip()
    text = text.replace("uh", "").replace("um", "").strip()
    
    # Detect if it's a system query
    intent = detect_intent(text)
    
    if intent != 'unknown':
        # It's a system query - get detailed response
        response = process_query(text)
        
        # Generate voice summary (shorter version for speech)
        voice_summary = generate_voice_summary(response)
        
        return {
            'type': 'system_query',
            'intent': intent,
            'text_response': response,
            'voice_summary': voice_summary,
            'action_taken': 'system_status_check'
        }
    
    # General conversation - extract facts
    elif len(text) > 20:
        # Auto-extract potential facts
        subprocess.run([
            sys.executable, str(WORKSPACE / "memory" / "extract_facts.py"),
            text
        ], capture_output=True)
        
        return {
            'type': 'conversation',
            'text_response': "Got it. I've noted that for your weekly review.",
            'voice_summary': "Noted. I'll remember that.",
            'action_taken': 'fact_extraction'
        }
    
    else:
        return {
            'type': 'unknown',
            'text_response': "I'm listening. What would you like me to do?",
            'voice_summary': "I'm here. What do you need?",
            'action_taken': 'none'
        }


def generate_voice_summary(detailed_response):
    """Generate a concise version for voice output."""
    lines = detailed_response.split('\n')
    
    # Extract emoji status lines
    summaries = []
    for line in lines:
        if any(icon in line for icon in ['✅', '⚠️', '🚨']):
            # Clean up for voice
            voice_line = line.replace('✅', 'All good').replace('⚠️', 'Warning').replace('🚨', 'Alert')
            voice_line = voice_line.replace('💾', 'Disk').replace('🧠', 'Memory')
            voice_line = voice_line.replace('🌐', 'Network').replace('⚙️', 'n8n')
            summaries.append(voice_line)
    
    if summaries:
        return " ".join(summaries[:4])  # Max 4 items for voice
    
    # Fallback: first sentence
    return detailed_response.split('.')[0] + "."


def main():
    if len(sys.argv) < 2:
        print("Usage: voice_processor.py '/path/to/audio.ogg' 'transcribed text'")
        print("       voice_processor.py 'transcribed text'  (no audio file)")
        sys.exit(1)
    
    # Parse args
    if sys.argv[1].endswith('.ogg') or sys.argv[1].endswith('.mp3') or sys.argv[1].endswith('.wav'):
        audio_path = sys.argv[1]
        transcribed_text = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        audio_path = None
        transcribed_text = ' '.join(sys.argv[1:])
    
    # Process
    result = process_voice_command(transcribed_text, audio_path)
    
    # Output as JSON for integration
    print(json.dumps(result, indent=2))
    
    # Optional: generate voice response file
    voice_file = WORKSPACE / "temp" / "voice_response.aiff"
    voice_file.parent.mkdir(exist_ok=True)
    
    if text_to_speech(result['voice_summary'], voice_file):
        result['voice_file'] = str(voice_file)
    
    # Re-print with voice file path
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
