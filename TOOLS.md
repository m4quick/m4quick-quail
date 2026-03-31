# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin
- pihole → 192.168.1.57, user: pi, container: pihole
  - **Web UI:** http://192.168.1.57/admin
  - **Web Password:** Ver!zon723640695
  - **API:** http://192.168.1.57/api (session-based auth)
  - **DHCP:** Built-in (active), range 192.168.1.101-200
  - **Monitor:** /usr/local/bin/pihole-dhcp-monitor.sh (every 5 min)
  - **Docker:** pihole/pihole:latest (not systemd service)
  - Old isc-dhcp-server: DISABLED

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Preferences

**Local-First Policy**
- Always prefer local tools and self-hosted solutions over cloud APIs
- Use Ollama (local LLM) as primary model — no token costs, no rate limits
- Video/audio processing via MoviePy/ffmpeg/PIL — no cloud rendering
- File operations stay on local filesystem
- Web search/downloads only when current external data is required
- Prefer open-source assets over subscription services

---

### Telegram Voice + Mac Audio

**Inbound (You → Me):**
- Voice messages transcribed via Whisper (local, private)
- Works great for hands-free communication when away from Mac

**Outbound (Me → You):**
- **Telegram text:** Primary reply channel
- **Mac audio (via `say`):** Simultaneous spoken announcements when you're near the Mac
- Use both channels for notifications, timers, alerts

**Voice preference:** Kate (macOS built-in, female). Alternatives: Samantha, Alex, ElevenLabs.

---

### Daily Report Automation

**Status:** ✅ Active — using macOS Mail (not Himalaya)
**Script:** `/Users/mirzaie/.openclaw/scripts/generate_daily_report.sh`
**Schedule:** Daily at 8:00 AM ET via LaunchAgent
**LaunchAgent:** `/Users/mirzaie/Library/LaunchAgents/com.openclaw.daily-report.plist`
**Sends via:** macOS Mail app (mmirzaie@msn.com)

**Includes:**
- System uptime & macOS version
- Disk usage
- Memory stats (total/used)
- Top CPU/memory processes
- External IP
- Pi-hole detailed stats (queries, blocks, top devices)
- AI burn rate (placeholder)

**Manual run:**
```bash
/Users/mirzaie/.openclaw/scripts/generate_daily_report.sh
```

**Check logs:**
```bash
tail /tmp/daily_report.out
tail /tmp/daily_report.err
```

**To disable:**
```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.daily-report.plist
```

---

### macOS Mail Access

**Status:** Full Disk Access granted ✅
**Accounts:**
- mmirzaie@msn.com (primary)
- Exchange
- Aliases: michael@mirzaie.com, quail@mirzaie.com

**Can do:**
- Read inbox/sent
- Generate summaries
- Send emails via AppleScript

**Example:**
```bash
osascript -e 'tell application "Mail" to count messages of inbox'
```

---

### Video Production Asset Management

**Location:** `~/M4Quick_Production/` (temporarily on main drive, move to Backup when permissions fixed)  
**Current Disk:** 753GB free (17% used) — **MONITOR CLOSELY**

**Folder Structure:**
```
~/M4Quick_Production/
├── 00_Projects/
│   ├── Quail_Hatching_2026/     ← Current video project
│   ├── OpenClaw_WebUI/          ← Demo video, screen recordings
│   └── PiHole_Monitor/          ← Future tutorial
├── 01_Footage/                   ← Raw camera files (by month)
│   ├── 2026-03/
│   ├── 2026-04/
│   └── 2026-05/
├── 02_Audio/                     ← Music, SFX, voiceover
├── 03_Graphics/                  ← Thumbnails, overlays, logos
├── 04_Exports/                   ← Final videos
│   ├── YouTube/
│   ├── Demo_Reels/
│   └── Social_Media/
├── 05_Archive/                   ← Completed projects
├── 06_Templates/                 ← Reusable assets
└── 07_Research/                  ← Scripts, ideas, analysis
    ├── Video_Scripts/
    ├── Thumbnail_Ideas/
    └── Competitor_Analysis/
```

**Usage Rules:**
1. **Track large files** — 4K footage fills ~20GB/hour
2. **Move to Archive** after project completes
3. **Monitor disk space** weekly — alert if <200GB free
4. **Backup target:** `/Volumes/Backup/M4Quick_Production/` (pending permission fix)

**Current Projects:**
| Project | Location | Status | Est. Size |
|---------|----------|--------|-----------|
| Quail Hatching | `00_Projects/Quail_Hatching_2026/` | Pre-production | 50GB |
| OpenClaw Demo | `00_Projects/OpenClaw_WebUI/` | Script phase | 10GB |

**Disk Monitor:**
```bash
# Check space
 df -h ~ | tail -1

# Alert if low
if [ $(df ~ | tail -1 | awk '{print $5}' | tr -d '%') -gt 80 ]; then echo "WARNING: Disk >80% full"; fi
```

---

### GitHub Architecture (Planned)

**Workflow:** Local (Gitea Docker) → Private GitHub → Public GitHub

**Repos:**
| Repo | Current | Target Public |
|------|---------|---------------|
| `openclaw-webui` | Private | Month 2-3 |
| `openclaw-scripts` | Private | Month 3-4 |
| `m4quick-farm-tools` | Private | Month 4-6 |
| `youtube-content` | Private | Never (private scripts) |

**Trigger:** Flip to public when companion video is edited and ready to upload

---

---

### Documentation Cross-Reference

| File | Purpose | Check When... |
|------|---------|---------------|
| `PROJECTS.md` | Active projects, status, next actions | Starting new work, checking what's pending |
| `SCHEDULE.md` | Recurring tasks, cron jobs, heartbeats | Wondering what's automated |
| `INTEGRATIONS.md` | How tools connect, system architecture | Adding new integrations |
| `MEMORY.md` | Long-term curated memory | Need context on past decisions |
| `memory/YYYY-MM-DD.md` | Daily raw logs | What happened on a specific day |

---

### Ultimate AI UI - Phase 1 Complete

**Status:** ✅ Phase 1 implemented (2026-03-31)
**Location:** `~/.openclaw/workspace/` scripts and memory system

#### Intelligent Heartbeat
**Script:** `scripts/intelligent_heartbeat.sh`  
**State:** `memory/heartbeat-state.json`

```bash
# Only alerts on state changes
~/.openclaw/workspace/scripts/intelligent_heartbeat.sh
# → HEARTBEAT_OK (silent) or "🚨 Pi-hole container is DOWN"
```

Smart behavior:
- Tracks last-known states
- Alerts once per incident (not every check)
- Recovery notifications
- Quiet hours support (23:00–08:00)

#### Natural Language System Queries
**Script:** `scripts/system_query.py`

```bash
# Ask in plain English
python3 ~/.openclaw/workspace/scripts/system_query.py "How's my disk?"
python3 ~/.openclaw/workspace/scripts/system_query.py "Check Pi-hole status"
python3 ~/.openclaw/workspace/scripts/system_query.py "Everything ok?"
```

Intents supported:
- Disk status
- Memory usage
- Pi-hole status
- n8n status
- Overall system health

#### Semantic Memory Extraction
**Scripts:**
- `memory/extract_facts.py` — Auto-extract facts from chats
- `memory/review_facts.py` — Weekly review interface

**Workflow:**
1. Conversations auto-extract facts (preferences, decisions, etc.)
2. Sunday 1 PM review: you approve/reject
3. Approved facts → MEMORY.md

```bash
# Review pending facts
python3 ~/.openclaw/workspace/memory/review_facts.py

# Stats
python3 ~/.openclaw/workspace/memory/review_facts.py --stats
```

**Privacy:** Filters out SSNs, credit cards, passwords automatically.

**Phase 2 Complete:** Voice-first, proactive intelligence, adaptive context

### Phase 2: Hybrid Interface

#### Voice Processor
**Script:** `scripts/voice_processor.py`

```bash
# Process voice command (from Whisper transcription)
python3 ~/.openclaw/workspace/scripts/voice_processor.py "How's my disk?"

# Returns JSON:
# {
#   "type": "system_query",
#   "text_response": "Full detailed response...",
#   "voice_summary": "Concise for speech...",
#   "voice_file": "/path/to/response.aiff"
# }
```

**Flow:** Voice note → Whisper → voice_processor → Intent → Action → Voice + Text response

#### Anomaly Detector (Proactive Intelligence)
**Script:** `scripts/anomaly_detector.py`
**State:** `memory/anomaly_trends.json`

```bash
# Detect anomalies before they become problems
python3 ~/.openclaw/workspace/scripts/anomaly_detector.py

# Example output:
# 📊 Disk usage spike detected: 85% (normal: 75% ± 3%)
# Suggestion: Run `du -sh ~/*/ | sort -hr | head -10`
```

**Detects:**
- Statistical anomalies (Z-score > 2.5)
- Rapid changes (>5% disk in 24h)
- Memory pressure increases

#### Context Bridge (Adaptive Context)
**Script:** `memory/context_bridge.py`

```bash
# Start session (get contextual greeting)
python3 ~/.openclaw/workspace/memory/context_bridge.py --start

# End session (record topic)
python3 ~/.openclaw/workspace/memory/context_bridge.py --end "MythBusters planning"

# See recent topics
python3 ~/.openclaw/workspace/memory/context_bridge.py --summary
```

**Contextual greetings:**
- <30 min: "Back already?"
- <2 hours: "Back to [topic]?"
- <1 day: "Good to see you again."
- >7 days: "It's been a while. How have you been?"

---

**Next:** Phase 3 (Intent-based automation, generated interfaces, autonomy spectrum)

---

Add whatever helps you do your job. This is your cheat sheet.
