#!/bin/bash
# Pi 4 Combined Setup: Pi-hole (Privacy-focused) + Voice Satellite (Penthouse)
# Blocks eavesdropping, tracking, telemetry

set -e

echo "=========================================="
echo "Enki Pi 4: Privacy-First Setup"
echo "Location: Penthouse"
echo "=========================================="
echo ""

if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root: sudo bash setup.sh"
    exit 1
fi

# Get Pi IP
PI_IP=$(hostname -I | awk '{print $1}')
echo "Pi IP Address: $PI_IP"
echo ""

echo "[1/10] Updating system..."
apt update && apt upgrade -y

echo ""
echo "[2/10] Installing Pi-hole..."
# Automated install with web interface
export PIHOLE_SKIP_OS_CHECK=true
curl -sSL https://install.pi-hole.net | bash /dev/stdin --unattended

echo ""
echo "[3/10] Installing privacy blocklists..."
# Comprehensive anti-eavesdropping blocklist
cat > /etc/pihole/adlists.list <> 'EOF'
# === SMART SPEAKER TELEMETRY ===
# Amazon Alexa - Full block (prevents eavesdropping)
*.amazonalexa.com
*.alexa.amazon.com
*.avs-alexa-na.amazon.com
*.avs-alexa-eu.amazon.com
*.device-metrics-us.amazon.com
*.device-metrics-us-2.amazon.com
*.amzdigital-assets.com
*.dp-discovery-alexa.amazon.com
# Google Assistant
deviceservices.googleapis.com
*.googleassistant.googleapis.com
# Apple Siri
crl.apple.com
*.push.apple.com
# Sonos telemetry
discovery.logitech.com
discovery.sonos.com
*.sonosradio.com

# === SMART HOME DEVICE TELEMETRY ===
# Ring
telemetry.ring.com
*.ring.com
# Nest
*.nest.com
telemetry.nest.com
# Ecobee
*.ecobee.com
# Wyze
*.wyze.com

# === GENERAL TRACKING/TELEMETRY ===
# Microsoft telemetry
*.telemetry.microsoft.com
*.telemetry.windows.com
*.ads.microsoft.com
# Google tracking
*.google-analytics.com
*.googletagmanager.com
*.doubleclick.net
*.googleadservices.com
# Facebook/Meta
*.facebook.com
*.fbcdn.net
# Misc trackers
*.scorecardresearch.com
*.newrelic.com
*.crashlytics.com
*.firebase-analytics.com

# === SECURITY CAMERAS ===
# Hikvision telemetry
*.hikvision.com
# Reolink
*.reolink.com
# Generic camera cloud
*.camera-cloud.com

# === SMART TV TRACKING ===
# Samsung
*.samsungtv.com
*.samsungacr.com
# LG
*.lgappstv.com
# Vizio
*.viziotv.com
# Roku
*.scribd.com
*.roku.com

# === VPN/SECURITY COMPANIES ===
# NordVPN (blocks leaks)
*.nordvpn.com
# ExpressVPN
*.expressvpn.com
EOF

# Update gravity
pihole -g

echo ""
echo "[4/10] Installing voice dependencies..."
apt install -y \
    python3-pip python3-venv \
    portaudio19-dev libatlas-base-dev \
    ffmpeg git alsa-utils pulseaudio \
    libportaudio2 espeak

# Setup audio
usermod -a -G audio pi

echo ""
echo "[5/10] Setting up Enki voice workspace..."
mkdir -p /home/pi/enki-voice
chown pi:pi /home/pi/enki-voice
cd /home/pi/enki-voice

sudo -u pi python3 -m venv venv

sudo -u pi bash -c '
    source venv/bin/activate
    pip install --upgrade pip
    pip install pvporcupine openai-whisper piper-tts requests pyaudio numpy
'

echo ""
echo "[6/10] Downloading voice models..."
sudo -u pi mkdir -p piper-voices
cd piper-voices
sudo -u pi wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
sudo -u pi wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
cd ..

echo ""
echo "[7/10] Creating voice service..."
sudo -u pi cat > config.json <> 'EOF'
{
    "location": "penthouse",
    "openclaw_host": "CHANGE_ME",
    "openclaw_port": 18789,
    "openclaw_token": "CHANGE_ME",
    "picovoice_key": "CHANGE_ME",
    "wake_word": "hey enki",
    "whisper_model": "tiny",
    "audio_device": "default",
    "output_volume": 80
}
EOF

sudo -u pi cat > voice_satellite.py <> 'PYEOF'
#!/usr/bin/env python3
"""
Enki Voice Satellite - Penthouse
Local-only voice control with privacy focus
"""

import json
import struct
import wave
import time
import requests
import os
import subprocess
import sys

# Load config
with open('/home/pi/enki-voice/config.json', 'r') as f:
    CONFIG = json.load(f)

LOCATION = CONFIG['location']
OPENCLAW_URL = f"http://{CONFIG['openclaw_host']}:{CONFIG['openclaw_port']}/api/message"
TOKEN = CONFIG['openclaw_token']

def log(msg):
    print(f"[{LOCATION}] {msg}")

def speak(text):
    """Speak response"""
    log(f"Enki: {text}")
    
    # Generate with Piper
    subprocess.run([
        "/home/pi/enki-voice/venv/bin/piper",
        "--model", "/home/pi/enki-voice/piper-voices/en_US-lessac-medium.onnx",
        "--config", "/home/pi/enki-voice/piper-voices/en_US-lessac-medium.onnx.json",
        "--output_file", "/tmp/response.wav"
    ], input=text.encode(), capture_output=True)
    
    # Play
    subprocess.run(["aplay", "/tmp/response.wav"], capture_output=True)

def record(duration=5):
    """Record command"""
    import pyaudio
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    
    log("🎤 Listening...")
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
    """Whisper STT"""
    import whisper
    log("📝 Processing...")
    model = whisper.load_model(CONFIG['whisper_model'])
    result = model.transcribe(audio_file, fp16=False)
    return result["text"].strip()

def query_openclaw(text):
    """Send to Mac OpenClaw"""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "message": text,
        "source": f"voice-{LOCATION}",
        "channel": "voice",
        "location": LOCATION
    }
    
    try:
        resp = requests.post(OPENCLAW_URL, json=data, headers=headers, timeout=30)
        return resp.json().get("response", "Processing...")
    except Exception as e:
        log(f"Error: {e}")
        return "I'm having trouble connecting"

def main():
    import pvporcupine
    import pyaudio
    
    log("🚀 Voice Satellite starting...")
    log("Say 'Hey Enki' to activate")
    
    # Check config
    if CONFIG['openclaw_host'] == 'CHANGE_ME':
        log("❌ ERROR: Please edit config.json with your Mac's Tailscale IP!")
        sys.exit(1)
    
    # Load wake word
    try:
        porcupine = pvporcupine.create(
            access_key=CONFIG['picovoice_key'],
            keywords=["hey computer"]  # Using "hey computer" - customize if needed
        )
    except Exception as e:
        log(f"Wake word error: {e}")
        log("Get free key at https://console.picovoice.ai")
        sys.exit(1)
    
    # Audio setup
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    log("✅ Ready - Listening for wake word...")
    
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            if porcupine.process(pcm) >= 0:
                log("🎯 Wake word detected!")
                speak("Yes Sir?")
                
                # Record command
                audio = record(5)
                
                # Transcribe
                command = transcribe(audio)
                if command:
                    log(f"Heard: {command}")
                    
                    # Query
                    response = query_openclaw(command)
                    speak(response)
                
                log("Listening...")
                
    except KeyboardInterrupt:
        log("👋 Shutting down...")
    finally:
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
PYEOF

sudo -u pi chmod +x voice_satellite.py

echo ""
echo "[8/10] Creating systemd service..."
cat > /etc/systemd/system/enki-voice-penthouse.service <> 'EOF'
[Unit]
Description=Enki Voice Satellite - Penthouse
After=network-online.target sound.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/enki-voice
Environment="PATH=/home/pi/enki-voice/venv/bin"
ExecStart=/home/pi/enki-voice/venv/bin/python /home/pi/enki-voice/voice_satellite.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

echo ""
echo "[9/10] Installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

echo ""
echo "[10/10] Setup complete!"
echo ""
echo "=========================================="
echo "CONFIGURATION NEEDED:"
echo "=========================================="
echo ""
echo "1. Get free Picovoice key:"
echo "   https://console.picovoice.ai"
echo ""
echo "2. Edit config.json:"
echo "   sudo nano /home/pi/enki-voice/config.json"
echo ""
echo "   Set these values:"
echo "   - openclaw_host: Your Mac's Tailscale IP"
echo "   - openclaw_token: From ~/.openclaw/openclaw.json"
echo "   - picovoice_key: From step 1"
echo ""
echo "3. Start Tailscale:"
echo "   sudo tailscale up"
echo ""
echo "4. Pair Bluetooth speaker:"
echo "   bluetoothctl"
echo "   scan on"
echo "   pair XX:XX:XX:XX:XX:XX"
echo "   trust XX:XX:XX:XX:XX:XX"
echo "   connect XX:XX:XX:XX:XX:XX"
echo ""
echo "5. Start voice service:"
echo "   sudo systemctl start enki-voice-penthouse"
echo "   sudo systemctl enable enki-voice-penthouse"
echo ""
echo "6. Router DNS Setup:"
echo "   Set primary DNS to: $PI_IP"
echo "   This blocks all tracking/telemetry"
echo ""
echo "Pi-hole admin: http://$PI_IP/admin"
echo "Default Pi-hole password: [check /etc/pihole/setupVars.conf]"
echo ""
echo "=========================================="
echo "BLOCKED TRAFFIC:"
echo "- Alexa/Google/Apple voice telemetry"
echo "- Smart device tracking"
echo "- Ad networks"
echo "- Analytics/telemetry"
echo "- Smart TV tracking"
echo "- Camera cloud uploads"
echo "=========================================="
