#!/usr/bin/env python3
"""
Voice Mic - Live microphone capture for OpenClaw
Records from default mic, transcribes with Whisper, processes with voice_processor

Usage:
    python3 scripts/voice_mic.py              # Record 5 seconds, auto-transcribe
    python3 scripts/voice_mic.py --duration 10  # Record 10 seconds
    python3 scripts/voice_mic.py --continuous     # Continuous mode (Ctrl+C to stop)
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
TEMP_DIR = WORKSPACE / "temp"

def get_default_mic():
    """Get default macOS audio input device."""
    try:
        result = subprocess.run(
            ['ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''],
            capture_output=True, text=True, timeout=5
        )
        # Parse output for input devices
        output = result.stderr
        lines = output.split('\n')
        
        # Find default mic (usually index 0 for input)
        for line in lines:
            if '[0]' in line and 'microphone' not in line.lower():
                return "0"  # Default input
        return "0"
    except Exception:
        return "0"

def record_audio(duration=5, output_path=None):
    """Record audio from default microphone using ffmpeg."""
    if output_path is None:
        TEMP_DIR.mkdir(exist_ok=True)
        output_path = TEMP_DIR / f"mic_recording_{int(time.time())}.wav"
    
    device = get_default_mic()
    
    print(f"🎤 Recording for {duration} seconds... (speak now)")
    
    try:
        subprocess.run([
            'ffmpeg', '-y',
            '-f', 'avfoundation',
            '-i', f':{device}',  # Input device (audio only)
            '-t', str(duration),
            '-ar', '16000',      # Whisper likes 16kHz
            '-ac', '1',          # Mono
            '-c:a', 'pcm_s16le',
            str(output_path)
        ], capture_output=True, check=True)
        
        print(f"✅ Saved: {output_path}")
        return Path(output_path)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Recording failed: {e}")
        return None

def transcribe_whisper(audio_path):
    """Transcribe audio using Whisper."""
    print("📝 Transcribing with Whisper...")
    
    try:
        result = subprocess.run(
            ['whisper', str(audio_path), '--model', 'tiny', '--language', 'en', '--output_format', 'txt', '--output_dir', str(TEMP_DIR)],
            capture_output=True, text=True, timeout=60
        )
        
        # Whisper creates a .txt file
        txt_file = audio_path.with_suffix('.txt')
        if txt_file.exists():
            text = txt_file.read_text().strip()
            # Cleanup
            txt_file.unlink(missing_ok=True)
            return text
        else:
            return ""
            
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return ""

def process_voice(transcribed_text):
    """Send to voice_processor for intent processing."""
    sys.path.insert(0, str(WORKSPACE / "scripts"))
    
    try:
        from voice_processor import process_voice_command
        result = process_voice_command(transcribed_text)
        return result
    except Exception as e:
        return {
            'error': str(e),
            'text_response': f"I heard: '{transcribed_text}' but processing failed."
        }

def speak_response(text):
    """Speak response using macOS say command."""
    print(f"🔊 Enki: {text}")
    subprocess.run(['say', '-v', 'Daniel', text], capture_output=True)

def main():
    parser = argparse.ArgumentParser(description='Live mic capture for OpenClaw')
    parser.add_argument('--duration', '-d', type=int, default=5, help='Recording duration in seconds (default: 5)')
    parser.add_argument('--continuous', '-c', action='store_true', help='Continuous mode (press Ctrl+C to stop)')
    args = parser.parse_args()
    
    if args.continuous:
        print("🎤 Continuous mode - Press Ctrl+C to stop")
        try:
            while True:
                audio_file = record_audio(duration=5)
                if audio_file:
                    text = transcribe_whisper(audio_file)
                    if text:
                        print(f"👤 You said: '{text}'")
                        result = process_voice(text)
                        speak_response(result['voice_summary'])
                    # Cleanup
                    audio_file.unlink(missing_ok=True)
        except KeyboardInterrupt:
            print("\n👋 Stopped")
    else:
        # Single capture
        audio_file = record_audio(duration=args.duration)
        if audio_file:
            text = transcribe_whisper(audio_file)
            if text:
                print(f"👤 You said: '{text}'")
                print("-" * 40)
                result = process_voice(text)
                print(f"\n📊 Response:")
                print(f"   Type: {result['type']}")
                print(f"   Action: {result['action_taken']}")
                print(f"   Text: {result['text_response'][:200]}...")
                
                # Speak it
                speak_response(result['voice_summary'])
                
                # Cleanup
                audio_file.unlink(missing_ok=True)
            else:
                print("❌ No speech detected")

if __name__ == '__main__':
    main()
