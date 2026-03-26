#!/bin/bash
# Pi 4 Voice Satellite Setup Script
# Run this on the Raspberry Pi (or via SSH from Mac)

set -e

echo "=== Enki Voice Satellite Setup ==="
echo "Setting up Pi 4 as voice hub for Sir..."
echo ""

# Update system
echo "[1/8] Updating system..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "[2/8] Installing dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    portaudio19-dev \
    libatlas-base-dev \
    ffmpeg \
    git \
    curl \
    alsa-utils \
    pulseaudio

# Create working directory
echo "[3/8] Creating workspace..."
mkdir -p ~/enki-voice
cd ~/enki-voice
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "[4/8] Installing Python packages..."
pip install --upgrade pip
pip install \
    pvporcupine \
    openai-whisper \
    piper-tts \
    requests \
    pyaudio \
    numpy

# Download Piper voice model
echo "[5/8] Downloading TTS voice..."
mkdir -p piper-voices
cd piper-voices
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
cd ..

# Create voice service script
echo "[6/8] Creating voice service..."
cat > voice_service.py << 'EOF'
#!/usr/bin/env python3
"""
Enki Voice Satellite Service
Runs on Pi 4, connects to OpenClaw Gateway on Mac
"""

import struct
import wave
import time
import requests
import pvporcupine
import whisper
import subprocess
import os

# Configuration - UPDATE THESE
OPENCLAW_HOST = "YOUR_MAC_TAILSCALE_IP"  # Mac's Tailscale IP
OPENCLAW_PORT = 18789
OPENCLAW_TOKEN = "YOUR_AUTH_TOKEN"

# Audio settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 512

def record_audio(duration=5):
    """Record audio from microphone"""
    import pyaudio
    
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )
    
    print("🎤 Recording...")
    frames = []
    for _ in range(0, int(SAMPLE_RATE / CHUNK_SIZE * duration)):
        data = stream.read(CHUNK_SIZE)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save to temp file
    wf = wave.open("/tmp/voice_command.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return "/tmp/voice_command.wav"

def transcribe_audio(audio_file):
    """Transcribe using Whisper"""
    print("📝 Transcribing...")
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file)
    return result["text"].strip()

def send_to_openclaw(text):
    """Send command to OpenClaw on Mac"""
    url = f"http://{OPENCLAW_HOST}:{OPENCLAW_PORT}/api/message"
    headers = {
        "Authorization": f"Bearer {OPENCLAW_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "message": text,
        "source": "pi-voice",
        "channel": "voice"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        return response.json().get("response", "No response")
    except Exception as e:
        print(f"Error connecting to OpenClaw: {e}")
        return "I'm having trouble connecting to Enki"

def speak_response(text):
    """Speak using Piper TTS"""
    print(f"🔊 Speaking: {text}")
    
    # Generate audio with Piper
    subprocess.run([
        "piper",
        "--model", "~/enki-voice/piper-voices/en_US-lessac-medium.onnx",
        "--config", "~/enki-voice/piper-voices/en_US-lessac-medium.onnx.json",
        "--output_file", "/tmp/response.wav"
    ], input=text.encode())
    
    # Play audio (to Bluetooth speaker)
    subprocess.run(["aplay", "/tmp/response.wav"])

def main():
    print("🚀 Enki Voice Satellite starting...")
    print("Say 'Hey Enki' to activate")
    
    # Load wake word
    porcupine = pvporcupine.create(keyword_paths=["hey-enki.ppn"])
    
    # Use default microphone
    import pyaudio
    pa = pyaudio.PyAudio()
    
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    try:
        while True:
            # Listen for wake word
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("\n🎯 Wake word detected!")
                
                # Record command
                audio_file = record_audio(duration=5)
                
                # Transcribe
                command = transcribe_audio(audio_file)
                print(f"Command: {command}")
                
                if command:
                    # Send to OpenClaw
                    response = send_to_openclaw(command)
                    
                    # Speak response
                    speak_response(response)
                
                print("\nListening for 'Hey Enki'...")
                
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
EOF

chmod +x voice_service.py

# Create systemd service for auto-start
echo "[7/8] Creating systemd service..."
sudo tee /etc/systemd/system/enki-voice.service > /dev/null << EOF
[Unit]
Description=Enki Voice Satellite
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/enki-voice
Environment="PATH=/home/pi/enki-voice/venv/bin"
ExecStart=/home/pi/enki-voice/venv/bin/python /home/pi/enki-voice/voice_service.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

echo "[8/8] Setup complete!"
echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Update voice_service.py with your Mac's Tailscale IP"
echo "2. Update with your OpenClaw auth token"
echo "3. Connect USB microphone (or pair Bluetooth mic)"
echo "4. Test: python3 voice_service.py"
echo "5. Enable auto-start: sudo systemctl enable enki-voice"
echo "6. Start service: sudo systemctl start enki-voice"
echo ""
echo "📁 Files installed in: ~/enki-voice/"
echo "🎤 Ready for voice control!"
