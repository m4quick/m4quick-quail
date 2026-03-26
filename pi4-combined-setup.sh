#!/bin/bash
# Pi 4 Combined Setup: Pi-hole + Voice Satellite
# Run this after Pi OS is installed

set -e

echo "=========================================="
echo "Enki Pi 4: Pi-hole + Voice Satellite"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root: sudo bash pi4-combined-setup.sh"
    exit 1
fi

echo "[1/10] Updating system..."
apt update && apt upgrade -y

echo ""
echo "[2/10] Installing Pi-hole..."
echo "This will ask you some questions..."
sleep 2
# Automated Pi-hole install
curl -sSL https://install.pi-hole.net | bash

echo ""
echo "[3/10] Configuring Pi-hole blocklists for Alexa..."
# Add Alexa domains to blocklist
cat >> /etc/pihole/adlists.list <> 'EOF'
# Block Alexa telemetry
discovery.logitech.com
discovery.sonos.com
# Block Amazon ad/tracking (keep shopping functional)
# Full Alexa block - uncomment if you want COMPLETE block:
# amazonalexa.com
# alexa.amazon.com
# amzdigital-assets.com
# device-metrics-us.amazon.com
EOF

# Update gravity (Pi-hole's blocklist)
pihole -g

echo ""
echo "[4/10] Installing voice dependencies..."
apt install -y \
    python3-pip \
    python3-venv \
    portaudio19-dev \
    libatlas-base-dev \
    ffmpeg \
    git \
    alsa-utils \
    pulseaudio \
    libportaudio2

# Create voice user
usermod -a -G audio pi

echo ""
echo "[5/10] Setting up Enki voice workspace..."
mkdir -p /home/pi/enki-voice
chown pi:pi /home/pi/enki-voice
cd /home/pi/enki-voice

# Create virtual environment
sudo -u pi python3 -m venv venv

# Install packages
sudo -u pi bash -c '
    source venv/bin/activate
    pip install --upgrade pip
    pip install pvporcupine openai-whisper piper-tts requests pyaudio numpy
'

echo ""
echo "[6/10] Downloading voice model..."
sudo -u pi mkdir -p piper-voices
cd piper-voices
sudo -u pi wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
sudo -u pi wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
cd ..

echo ""
echo "[7/10] Creating voice service..."
sudo -u pi cat > voice_service.py <> 'EOF'
#!/usr/bin/env python3
"""
Enki Voice Satellite - Local Only
Connects to OpenClaw on Mac via Tailscale
"""

import struct
import wave
import time
import requests
import os
import subprocess
import threading
import queue

# CONFIGURATION - UPDATE THESE
OPENCLAW_HOST = "100.x.x.x"  # Mac's Tailscale IP
OPENCLAW_PORT = 18789
OPENCLAW_TOKEN = "your-token-here"

# Use tiny Whisper model for Pi 4 (fast, low memory)
WHISPER_MODEL = "tiny"

def speak(text):
    """Speak using Piper TTS to Bluetooth speaker"""
    print(f"🔊 Enki: {text}")
    
    # Generate speech
    subprocess.run([
        "/home/pi/enki-voice/venv/bin/piper",
        "--model", "/home/pi/enki-voice/piper-voices/en_US-lessac-medium.onnx",
        "--config", "/home/pi/enki-voice/piper-voices/en_US-lessac-medium.onnx.json",
        "--output_file", "/tmp/response.wav"
    ], input=text.encode(), capture_output=True)
    
    # Play to default audio (should be Bluetooth speaker)
    subprocess.run(["aplay", "/tmp/response.wav"], capture_output=True)

def record_command(duration=5):
    """Record audio command"""
    import pyaudio
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    
    print("🎤 Listening...")
    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save
    wf = wave.open("/tmp/command.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return "/tmp/command.wav"

def transcribe(audio_file):
    """Transcribe with Whisper"""
    import whisper
    
    print("📝 Processing speech...")
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio_file, fp16=False)
    return result["text"].strip()

def send_to_openclaw(text):
    """Send to Mac OpenClaw"""
    url = f"http://{OPENCLAW_HOST}:{OPENCLAW_PORT}/api/message"
    headers = {
        "Authorization": f"Bearer {OPENCLAW_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "message": text,
        "source": "pi-voice",
        "channel": "voice-satellite"
    }
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=30)
        return resp.json().get("response", "I'm thinking...")
    except Exception as e:
        print(f"Connection error: {e}")
        return "I'm having trouble reaching Enki"

def main():
    print("🚀 Enki Voice Satellite ready!")
    print("Say 'Hey Enki' to activate")
    print("Press Ctrl+C to stop")
    print("")
    
    # Load wake word
    import pvporcupine
    porcupine = pvporcupine.create(
        access_key="your-picovoice-key",  # Get free key from picovoice.ai
        keywords=["hey enki"]
    )
    
    import pyaudio
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    try:
        while True:
            # Listen for wake word
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            result = porcupine.process(pcm)
            if result >= 0:
                print("\n🎯 Wake word detected!")
                speak("Yes Sir?")
                
                # Record command
                audio = record_command(5)
                
                # Transcribe
                command = transcribe(audio)
                if command:
                    print(f"Command: {command}")
                    
                    # Get response from Enki
                    response = send_to_openclaw(command)
                    
                    # Speak it
                    speak(response)
                
                print("\nListening for 'Hey Enki'...")
                
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
EOF

sudo -u pi chmod +x voice_service.py

echo ""
echo "[8/10] Creating systemd service..."
cat > /etc/systemd/system/enki-voice.service <> 'EOF'
[Unit]
Description=Enki Voice Satellite
After=network-online.target
Wants=network-online.target

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

systemctl daemon-reload

echo ""
echo "[9/10] Getting Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

echo ""
echo "[10/10] Setup complete!"
echo ""
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo ""
echo "1. Edit voice_service.py:"
echo "   - Set OPENCLAW_HOST to Mac's Tailscale IP"
echo "   - Set OPENCLAW_TOKEN from ~/.openclaw/openclaw.json"
echo "   - Get free Picovoice key: https://picovoice.ai"
echo ""
echo "2. Start Tailscale:"
echo "   sudo tailscale up"
echo ""
echo "3. Connect Bluetooth speaker:"
echo "   bluetoothctl"
echo "   scan on"
echo "   pair XX:XX:XX:XX:XX:XX"
echo "   connect XX:XX:XX:XX:XX:XX"
echo ""
echo "4. Test voice:"
echo "   sudo systemctl start enki-voice"
echo ""
echo "5. Enable auto-start:"
echo "   sudo systemctl enable enki-voice"
echo ""
echo "6. Configure router:"
echo "   Set DNS to this Pi's IP: $(hostname -I | awk '{print $1}')"
echo ""
echo "Pi-hole admin: http://$(hostname -I | awk '{print $1}')/admin"
echo "=========================================="
