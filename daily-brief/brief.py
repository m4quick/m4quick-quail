#!/usr/bin/env python3
"""Daily Brief Generator - Flask Service"""

import subprocess
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, jsonify

import config

app = Flask(__name__)


def get_weather():
    """Fetch weather from wttr.in"""
    try:
        url = f"https://wttr.in/{config.WEATHER_LOCATION}?format=4&u"
        headers = {'User-Agent': 'Mozilla/5.0 (Daily-Brief/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Weather service returned status {response.status_code}"
    except requests.exceptions.Timeout:
        return "Weather service timed out (check internet connection)"
    except requests.exceptions.ConnectionError:
        return "Weather service unreachable (check internet connection)"
    except Exception as e:
        return f"Weather error: {str(e)}"


def get_pihole_status():
    """Check Pi-hole DNS status"""
    try:
        result = subprocess.run(
            ['nc', '-z', '-w', '5', config.PIHOLE_IP, '53'],
            capture_output=True
        )
        return "✅ Online" if result.returncode == 0 else "❌ Unreachable"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def generate_brief():
    """Generate the daily brief"""
    now = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p")
    
    brief = f"""# Daily Brief — {now}

## Weather
{get_weather()}

## Network Health
**Pi-hole DNS:** {get_pihole_status()}

## System Status
- Brief generated from: {config.WEATHER_LOCATION}
- Pi-hole IP: {config.PIHOLE_IP}
"""
    return brief


def send_email(subject, body):
    """Send email via SMTP"""
    if not config.EMAIL_ENABLED:
        return False, "Email disabled"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = config.SMTP_USER
        msg['To'] = config.EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASS)
        server.send_message(msg)
        server.quit()
        return True, "Email sent"
    except Exception as e:
        return False, str(e)


def send_telegram(message):
    """Send Telegram message"""
    if not config.TELEGRAM_ENABLED:
        return False, "Telegram disabled"
    
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': config.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200, response.text
    except Exception as e:
        return False, str(e)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


@app.route('/generate', methods=['POST'])
def generate():
    """Generate and send daily brief"""
    brief = generate_brief()
    
    results = {
        'brief': brief,
        'email': None,
        'telegram': None,
        'timestamp': datetime.now().isoformat()
    }
    
    # Try email
    if config.EMAIL_ENABLED:
        success, msg = send_email("Daily Brief", brief)
        results['email'] = {'success': success, 'message': msg}
    
    # Try Telegram
    if config.TELEGRAM_ENABLED:
        success, msg = send_telegram(brief)
        results['telegram'] = {'success': success, 'message': msg}
    
    return jsonify(results)


@app.route('/preview', methods=['GET'])
def preview():
    """Preview brief without sending (JSON)"""
    return jsonify({
        'brief': generate_brief(),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/', methods=['GET'])
def html_view():
    """HTML view of daily brief (browser-friendly)"""
    brief = generate_brief()
    # Convert markdown to simple HTML
    html = brief.replace('\n', '<br>')
    html = html.replace('# ', '<h1>').replace('## ', '<h2>')
    html = html.replace('**', '<b>').replace('**', '</b>')
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Daily Brief</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .weather {{ font-size: 1.2em; background: #f5f5f5; padding: 15px; border-radius: 8px; }}
        .status {{ background: #e8f5e9; padding: 10px 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    {html}
    <br><br>
    <small><a href="/preview">View JSON</a> | <a href="/health">Health Check</a></small>
</body>
</html>"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
