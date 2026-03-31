# SCHEDULE.md — Recurring Tasks & Automations

_All scheduled tasks, heartbeats, and recurring automations. Checked on startup._

## Daily Automations

### 1. Daily Report (System Status)
**When:** 8:00 AM ET daily  
**What:** Generates system report (uptime, disk, memory, Pi-hole stats, project status)  
**How:** macOS LaunchAgent  
**Script:** `~/.openclaw/scripts/generate_daily_report.sh`  
**Output:** `/tmp/daily_report_YYYY-MM-DD.txt`  
**Delivery:** Email via macOS Mail app

**Reliability Features:**
- **Retry Logic:** 3 attempts with exponential backoff (30s → 60s → 120s)
- **Failure Notification:** Telegram alert if all retries fail
- **Error Capture:** Logs AppleScript errors for debugging

**To verify running:**
```bash
launchctl list | grep openclaw
```

**To disable:**
```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.daily-report.plist
```

**Recent Changes:**
- 2026-03-30: Added retry logic and Telegram failure alerts (Mail timeout at 08:02 caused missing report)

---

## Heartbeat Checks (Periodic)

### Network Infrastructure Check
**When:** 2x daily (defined in HEARTBEAT.md)  
**What:** 
- Check Pi-hole DNS/DHCP responding
- Verify Alexa devices have leases
- Check for excessive blocked queries

**Action items:**
- If Pi-hole DHCP down → `sudo systemctl restart pihole-FTL`
- If Alexa offline → Check DHCP lease expiration

---

## Manual Triggers (On-Demand)

### Daily Brief Service
**Endpoint:** `http://localhost:5000` (when running)  
**Routes:**
- `/health` — Service status
- `/preview` — Generate brief (no send)
- `/generate` — Generate and deliver

**To start:**
```bash
cd ~/.openclaw/workspace/daily-brief
docker-compose up -d
```

---

## Agent Responsibilities

| Task | Primary Agent | Backup |
|------|-------------|--------|
| Daily system report | LaunchAgent (n8n?) | Manual run |
| Network health check | Heartbeat (me) | — |
| Email sending | Himalaya CLI | — |
| Telegram notifications | OpenClaw gateway | — |

---

## Calendar Integration (Future)

- [ ] Check calendar for upcoming events
- [ ] Morning brief with day's schedule
- [ ] Reminders for recurring meetings

