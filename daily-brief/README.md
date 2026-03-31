# Daily Brief Service

Flask-based daily brief generator running in Docker on Mac.

## Quick Start

```bash
# Build and start
cd daily-brief
docker-compose up --build -d

# Check health
curl http://localhost:5000/health

# Preview brief (no sending)
curl http://localhost:5000/preview

# Generate and send brief
curl -X POST http://localhost:5000/generate
```

## Configuration

Edit `docker-compose.yml` to enable delivery:

### Email (Gmail)
```yaml
- EMAIL_ENABLED=true
- SMTP_USER=you@gmail.com
- SMTP_PASS=your_app_password
- EMAIL_TO=recipient@email.com
```

### Telegram
```yaml
- TELEGRAM_ENABLED=true
- TELEGRAM_BOT_TOKEN=your_bot_token
- TELEGRAM_CHAT_ID=your_chat_id
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/preview` | GET | Preview brief without sending |
| `/generate` | POST | Generate and send brief |

## Scheduled Execution

memUbot can call the webhook:
```bash
curl -X POST http://localhost:5000/generate
```

Or use Mac cron:
```bash
0 8 * * * curl -X POST http://localhost:5000/generate
```
