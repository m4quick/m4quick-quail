import os

# Delivery settings
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')
EMAIL_TO = os.getenv('EMAIL_TO', '')

TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Pi-hole settings
PIHOLE_IP = os.getenv('PIHOLE_IP', '192.168.1.57')

# Weather location
WEATHER_LOCATION = os.getenv('WEATHER_LOCATION', 'Virginia+USA')
