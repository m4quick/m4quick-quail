# MEMORY.md - Long-Term Memory

## Personal Preferences
- **Favorite color:** Blue

---

## Active Projects

### M4Quick Quail Farm (YouTube/Monetization)
**Goal:** Build quail-focused YouTube channel with affiliate revenue

**Assets Created:**
- **Amazon Associates ID:** m4quickquail-20 (approved, ~4-10% commission)
- **Website:** https://m4quick.github.io/m4quick-quail
- **Video Ready:** QuailHatchVideo_v23d_TRANSITIONS.mp4 (52MB)
- **Channel:** M4Quick Quail Farm (@m4quick) — pending creation

**Content Strategy:**
- Myth Busters style videos (8 myths identified)
- First episode script: "Myth BUSTED: Quail DON'T Need Expensive Incubators"
- 5-act structure: Hook → Small Test → Build → Climax → Verdict

**Affiliate Products Listed:**
| Product | Price Range | Link Status |
|---------|-------------|-------------|
| Brinsea Mini II Incubator | $300-400 | ✅ With tracking ID |
| Little Giant Incubator | $50-80 | ✅ With tracking ID |
| Manna Pro Gamebird Feed | $25-40 | ✅ With tracking ID |
| Quail Cage 6-Layer | $100-150 | ✅ With tracking ID |
| Automatic Quail Feeder | $20-30 | ✅ With tracking ID |

**Tools Created:**
- `amazon-link.sh` — Generate affiliate links on demand
- `yt-affiliate.sh` — Create YouTube descriptions with links
- `youtube-descriptions.txt` — 4 copy-paste templates

**Status:** Revenue infrastructure complete, waiting on channel creation + first video upload

---

## Infrastructure

### Network (Pi-hole)
- **Hardware:** Raspberry Pi 4 @ 192.168.1.57
- **Admin Panel:** http://192.168.1.57/admin
- **Password:** Ver!zon723640695
- **Install Method:** Docker with host networking
- **DHCP:** Built-in to Pi-hole (not isc-dhcp-server — migrated Mar 25)
- **Blocklist:** StevenBlack Unified Hosts (~86,000 domains)

**Health Monitoring:**
- Script: `/usr/local/bin/pihole-dhcp-monitor.sh`
- Timer: Runs every 5 minutes via systemd
- Auto-restart if DHCP fails

### Daily Report Automation
- **Schedule:** Daily at 8:00 AM ET
- **Script:** `/Users/mirzaie/.openclaw/scripts/generate_daily_report.sh`
- **Delivery:** macOS Mail app (mmirzaie@msn.com)
- **Features:** Retry logic (3 attempts, exponential backoff)
- **Includes:** System status, Pi-hole stats, weather, burn rate, project updates

### macOS Mail Integration
- **Status:** Full Disk Access granted ✅
- **Accounts:** mmirzaie@msn.com (primary), Exchange, aliases
- **Method:** AppleScript (not himalaya — switched for OAuth2 compatibility)

---

## Ecosystem Roles (Three-Tool Setup)

| Tool | Purpose | My Role |
|------|---------|---------|
| **memU Bot** | Memory & planning | Do not duplicate — use for task tracking |
| **n8n** | Scheduled execution | Trigger via webhooks when needed |
| **Enki (me)** | Complex ad-hoc tasks | Reasoning, tools, one-off execution |

**Clarification:** n8n is still running (port 5678) — memUbot's claim of "removing n8n" was incorrect.

---

## Technical Decisions

### Video Production
- **Tool:** MoviePy 1.0.3 + PIL (avoiding ffmpeg drawtext issues)
- **Format:** 9:16 vertical (1080x1920), 30s, 30fps
- **Text:** White fill + black stroke (stroke_width=4), multi-line for readability
- **Audio:** YouTube Audio Library (royalty-free)

**Lesson Learned:** v5 video contaminated with non-quail content — always verify source clips before rendering.

### WebUI Development
- **Framework:** Flask backend + vanilla JS frontend
- **Location:** `/Users/mirzaie/.openclaw/workspace/openclaw-webui/`
- **Status:** Real OpenClaw integration with memory bridge

**Cross-Device Issue:** Buttons greyed out on HTTP-over-IP (browser secure context requirement)
**Solution:** Use `http://127.0.0.1:5001` (localhost) or Tailscale serve for HTTPS

---

## March 30-31, 2026: Session Continuity & AR Dashboard

**Problem Discovered:** Every OpenClaw session starts fresh — no memory of previous conversations. "Fresh baby problem."

**Root Cause:** WebUI generated new random `session_id` for each message. OpenClaw Gateway maintains sessions per `session_key`, but client wasn't reusing them.

**Solution Built:**

### 1. Memory Bridge Architecture
- **File:** `~/.openclaw/memory/sir-context.json` — persistent identity
- **Module:** `~/.openclaw/workspace/openclaw-webui/memory_bridge.py`
- **Mechanism:** Injects context as system prompt on every API call

**Context includes:**
- Identity (Sir, Virginia, America/New_York)
- Active projects (quail hatching, WebUI AR, daily reports)
- Recent facts (Day 7 incubation, hatch April 8-9, Quest 3 tested)
- Preferences (direct communication, local-first policy)
- Ongoing conversations across channels

### 2. WebUI Session Fix
- **Before:** `session_id = uuid.uuid4()` (new ID every message)
- **After:** Consistent `sir-main-session` + `localStorage` persistence
- **Result:** Cross-call continuity via `x-openclaw-session-key` header

### 3. AR Dashboard (Quest 3)
- **URL:** `http://192.168.1.168:5001/ar`
- **Features:** WebXR, hand tracking (MediaPipe), voice I/O, floating 3D panels
- **Tested:** Quest 3 Browser — works, but limited vs. native

**Technical Learning:**
- KV cache = GPU memory optimization (different problem)
- App-level session continuity = API client responsibility
- OpenClaw Gateway DOES support persistent sessions via `session_key`

**New Files:**
- `worklog/2026-03-30.md` — Daily process tracking (started)
- `memory/sir-context.json` — Cross-channel persistent context
- `quest3-setup.md` — Meta Quest 3 browser setup instructions

---

## GitHub Strategy

**Workflow:** Local (Gitea Docker) → Private GitHub → Public GitHub

**Repos Planned:**
| Repo | Current | Target Public |
|------|---------|---------------|
| openclaw-webui | Private | Month 2-3 (with companion video) |
| openclaw-scripts | Private | Month 3-4 |
| m4quick-farm-tools | Private | Month 4-6 |
| youtube-content | Private | Never (private scripts) |

**Trigger:** Flip to public when companion video is edited and ready to upload.

---

## Current Quail Status
- Eggs in incubator (hatch expected April 8-9)
- Day 7 as of last check (March 30)

---

## Files Referenced
- Daily logs: `memory/YYYY-MM-DD.md`
- Project status: `PROJECTS.md`
- Schedule/automations: `SCHEDULE.md`
- System architecture: `INTEGRATIONS.md`
- Tools/credentials: `TOOLS.md`
- Process tracking: `worklog/YYYY-MM-DD.md` (NEW)
