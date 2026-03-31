# HEARTBEAT.md - Intelligent Periodic Checks

## Philosophy
**Silent success. Only speak when something changes or needs attention.**

This heartbeat uses stateful monitoring — it remembers what's "normal" and only alerts you when:
- Something breaks that was working
- Something recovers that was broken
- Critical thresholds are crossed
- Daily digest is due

## Quick Status
```bash
# Run intelligent check manually
~/.openclaw/workspace/scripts/intelligent_heartbeat.sh

# Check current state
cat ~/.openclaw/workspace/memory/heartbeat-state.json | python3 -m json.tool
```

## Monitored Systems

| System | Check | Alert Trigger |
|--------|-------|---------------|
| **Pi-hole** | Container status via SSH | DOWN → UP, UP → DOWN |
| **Disk Usage** | `df ~` | >80% (warn), >90% (critical), recovery |
| **n8n** | Docker container | not running → running, running → not running |
| **Memory** | `memory_pressure` | <50% warning, recovery |
| **Daily Report** | Last sent time | If not sent by 9 AM |

## Alert Behavior

**During Quiet Hours (23:00–08:00):**
- Critical alerts: Sent immediately
- Warning alerts: Queued, sent at 08:00
- Recovery alerts: Queued, sent at 08:00

**Normal Hours:**
- All alerts sent immediately

**No Alert Scenario:**
- Everything working as expected = `HEARTBEAT_OK`

## State File
Location: `~/.openclaw/workspace/memory/heartbeat-state.json`

Tracks:
- Last known states of all systems
- Alert flags (prevent spam)
- Timestamps of last checks
- Configuration thresholds

## Commands Reference

### Pi-hole (Docker on 192.168.1.57)
```bash
# Check container
ssh pi@192.168.1.57 'sudo docker ps | grep pihole'

# Restart if needed
ssh pi@192.168.1.57 'sudo docker restart pihole'
```

### Disk/Memory
```bash
# Disk
df -h ~

# Memory pressure
memory_pressure
```

### n8n
```bash
# Check
docker ps | grep n8n

# Restart
docker restart n8n
```

## Phase 2 Integration (Proactive Intelligence)

**Anomaly Detection:** Runs alongside heartbeat checks
```bash
# Detect unusual patterns
python3 ~/.openclaw/workspace/scripts/anomaly_detector.py

# Full check including proactive alerts
python3 ~/.openclaw/workspace/scripts/anomaly_detector.py --check-all
```

**Context Awareness:** Session bridging
```bash
# Start of session
python3 ~/.openclaw/workspace/memory/context_bridge.py --start

# End of session (record topic)
python3 ~/.openclaw/workspace/memory/context_bridge.py --end "Pi-hole setup"
```

## History
- **2026-03-31:** Phase 2 — Anomaly detection, context bridge, voice processor
- **2026-03-31:** Phase 1 — Migrated to intelligent heartbeat with state tracking
- **2026-03-29:** Fixed Pi-hole monitoring — discovered it's Dockerized
- **2026-03-25:** Added `pihole-dhcp-monitor.service/timer`
