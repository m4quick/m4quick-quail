# PROJECTS.md — Active Work Tracker

_Tracks current projects, status, and next actions. Updated whenever work starts/completes._

## Current Projects

### 1. Daily Report Automation
**Status:** ✅ Complete  
**Last updated:** 2026-03-30

**Configuration Documentation:**
```
Project: Daily_Report_Automation
├── Location: ~/.openclaw/scripts/generate_daily_report.sh
├── GitHub Repo: github.com/m4quick-studio/openclaw-scripts (NOT YET CREATED)
│   └── Target: Private → Public (Month 3-4)
├── LaunchAgent: ~/Library/LaunchAgents/com.openclaw.daily-report.plist
├── Logs: /tmp/daily_report.{out,err}
├── Dependencies:
│   - macOS Mail (Full Disk Access granted)
│   - Pi-hole SSH access (pi@192.168.1.57)
│   - PROJECTS.md (for status updates)
├── Schedule: Daily 8:00 AM ET
├── Recipients: mmirzaie@msn.com
├── Disk Estimate: 1MB (script only)
└── Status: Active, runs autonomously
```

**What:** Automated daily system reports at 8 AM  
**Components:**
- ✅ Report generation script (`~/.openclaw/scripts/generate_daily_report.sh`)
- ✅ LaunchAgent scheduled (runs daily 8 AM)
- ✅ Email delivery via macOS Mail (switched from Himalaya)

**Includes:**
- System uptime & macOS version
- Disk usage
- Memory stats (total/used)
- Top CPU/memory processes
- External IP
- Pi-hole detailed stats (queries, blocks, top devices)
- AI burn rate (placeholder)
- Project status from PROJECTS.md

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

### 2. Daily-Brief Flask Service
**Status:** ✅ Built, Ready to Deploy  
**Last updated:** 2026-03-29

**What:** Web service for on-demand daily brief generation  
**Location:** `~/.openclaw/workspace/daily-brief/`  
**Endpoints:**
- `GET /health` — Service status
- `GET /preview` — Generate brief, return as text
- `POST /generate` — Generate and send via configured method

**Features:**
- Weather (wttr.in)
- Pi-hole status
- Email/Telegram delivery
- Dockerized deployment

**Next action:** Decide deployment method (n8n webhook vs. standalone)

---

### 3. Multi-Agent Memory Integration
**Status:** 🔄 In Discussion  
**Last updated:** 2026-03-29

**What:** Share context between memU, n8n, and Enki  
**Blocker:** memUbot hosted service is paid API — need local file sync instead  
**Options:**
- Shared workspace directory
- Symlinked memory folders
- n8n as router/bridge

**Next action:** Test if memUbot can write to local files

---

### 4. Email Setup (Himalaya)
**Status:** ⏳ Configured, Needs Password  
**Last updated:** 2026-03-27

**What:** CLI email client for sending/receiving  
**Config:** `~/.config/himalaya/config.toml` (wizard-generated)  
**Account:** mmirzaie@msn.com (Outlook)  
**Blocker:** Password not stored in keychain — keychain dialogs caused issues

**Next action:** Store password directly in config file temporarily, or retry keychain with proper permissions

---

### 5. Configuration & Documentation System
**Status:** ⏳ Planned  
**Last updated:** 2026-03-30

**What:** Document system configurations, asset structures, and dependencies  
**Scope:**
- Video production folder structure (`~/M4Quick_Production/`)
- GitHub repo architecture (Local → Private → Public)
- Physical asset tracking (incubator logs, equipment inventory)
- Cross-project dependencies

**Deliverables:**
- [ ] Configuration templates for new projects
- [ ] Asset tracking spreadsheet/system
- [ ] Dependency mapping (which projects rely on which)
- [ ] Documentation standards

**Depends on:** 
- External storage permission fix (see Backlog)
- Git server setup (Gitea)

**Next action:** Design configuration templates after storage issue resolved

---

## Backlog (Approved, Not Started)

_Curated from IDEAS.md. Items here are committed but not active._

- [ ] Pi-hole monitoring dashboard
- [ ] Alexa integration scripts
- [ ] **External Storage Permission Fix** — `Backup` drive permissions blocking M4Quick_Production folder creation
  - **Impact:** Video assets temporarily on main drive (753GB free)
  - **Priority:** Medium — can work around for now
  - **Solution:** Either fix permissions or use alternative storage

**Curation flow:** IDEAS.md (raw) → Review → Backlog (vetted) → Active

---

## Configuration Standards

**Purpose:** Document how system configurations, asset structures, and project dependencies are tracked.

### Asset Tracking System

**Current Structure:** `~/M4Quick_Production/`
```
00_Projects/        → Active video/code projects
01_Footage/         → Raw camera files (by month)
02_Audio/           → Music, SFX, voiceover
03_Graphics/        → Thumbnails, overlays
04_Exports/         → Final videos
05_Archive/         → Completed projects
06_Templates/       → Reusable assets
07_Research/        → Scripts, analysis
```

**Disk Monitoring:**
- **Current location:** Main drive (753GB free)
- **Target location:** `/Volumes/Backup/M4Quick_Production/` (pending permission fix)
- **Alert threshold:** <200GB free
- **Check command:** `df -h ~ | tail -1`

### GitHub Architecture

**Workflow:** Local (Gitea Docker) → Private GitHub → Public GitHub

**Repos planned (m4quick-studio org):**
| Repo | Status | Public Timeline |
|------|--------|-----------------|
| openclaw-webui | Ready | Month 2-3 |
| openclaw-scripts | Ready | Month 3-4 |
| m4quick-farm-tools | Planned | Month 4-6 |

**Migration trigger:** Flip to public when companion video is edited and ready

---

## 🛠️ ACTIVE: OpenClaw WebUI Development

**Configuration Documentation:**
```
Project: OpenClaw WebUI
├── Location: ~/.openclaw/workspace/openclaw-webui/
├── GitHub Repo: github.com/m4quick-studio/openclaw-webui ✅ LIVE
│   ├── Current: Local only
│   ├── Target: Private → Public (Month 2-3)
│   └── Trigger: When demo video is edited
├── Demo Video: ~/M4Quick_Production/00_Projects/OpenClaw_WebUI/
│   ├── Script: TBD
│   ├── Raw: ~/M4Quick_Production/01_Footage/2026-04/
│   └── Export: ~/M4Quick_Production/04_Exports/YouTube/
├── Local Test: http://localhost:5001 ✅ RUNNING
├── Dependencies:
│   - Python 3.9+
│   - Flask (installed)
│   - OpenClaw integration (TODO)
├── Disk Estimate: 5GB (code + demo footage)
└── Status: Code pushed, running locally, needs OpenClaw integration + demo video
```

### Goal
Build a ChatGPT/Grok-style web interface for OpenClaw to enable local access and content delivery.

### Features
- Web-based chat interface (responsive design)
- Real-time streaming responses
- File upload/download support
- Voice input (Whisper integration)
- Voice output (TTS integration)
- Session history / memory
- Multi-model support selector

### Phases

**Phase 1: Core Chat Interface (Week 1-2)**
- Static HTML/CSS/JS frontend
- Flask backend with SSE streaming
- Basic message history
- Resources: Flask, HTML/CSS, JavaScript

**Phase 2: File & Voice Support (Week 3-4)**
- File upload handling
- Image analysis display
- Voice recording via browser
- Resources: Web Audio API, file handling

**Phase 3: Polish & Demo (Week 5-6)**
- Responsive mobile design
- Dark/light themes
- Demo video script
- Resources: Screen recording, editing

### Technical Stack
- Frontend: Vanilla JS + Tailwind CSS
- Backend: Flask (Python)
- Communication: Server-Sent Events (SSE)
- Deployment: Local server + optional Tailscale

### Next Action
Create GitHub repo, scaffold Flask app, basic HTML structure

---

## 🎬 ACTIVE: YouTube Content Calendar

### Series: "Quail Myth Busters"

**Configuration Documentation:**
```
Project: Quail_Hatching_2026
├── Location: ~/M4Quick_Production/00_Projects/Quail_Hatching_2026/
├── GitHub: Not yet (footage only, not code)
├── Dependencies:
│   - Incubator: Little Giant (existing)
│   - Camera: iPhone/Mac (to be determined)
│   - Editor: CapCut or Final Cut Pro
├── Disk Estimate: 50GB (4K footage, ~2-3 hours raw)
├── Raw Footage: ~/M4Quick_Production/01_Footage/2026-04/
├── Script: ~/M4Quick_Production/07_Research/Video_Scripts/myth_busters_ep1_script.md
├── Exports: ~/M4Quick_Production/04_Exports/YouTube/
└── Status: Pre-production
```

**Timeline Dependencies:**
- Hatch window: April 8-9, 2026
- Film window: April 8-12 (can't reschedule)
- Edit/publish: April 15, 2026

#### Episode 1: "Myth BUSTED: Quail DON'T Need Expensive Incubators"
**Publish Target:** April 15, 2026 (post-hatch)
**Resources Needed:**
- [ ] 3 incubators: cheap styrofoam ($30), mid-range ($100), expensive ($300)
- [ ] 30+ Coturnix quail eggs
- [ ] Temperature/humidity loggers
- [ ] Macro camera for pipping shots
- [ ] Video editing software (CapCut/Final Cut)

**Timeline:**
- Week 1: Script, equipment acquisition
- Week 2: Setup, begin incubation
- Week 3: Hatch day filming
- Week 4: Edit, thumbnail, publish

**Monetization:**
- Affiliate links (incubators, thermometers)
- YouTube Partner Program (1K subs, 4K watch hours)
- Sponsorships (farm supply brands)

#### Episode 2: "Myth BUSTED: Quail Are NOT Too Noisy for Backyards"
**Publish Target:** April 30, 2026
**Resources:**
- [ ] Decibel meter app/device
- [ ] Neighbor interview/consent
- [ ] Comparison: chickens, dogs, traffic
- [ ] Quiet quail setup demonstration

#### Episode 3: "Myth BUSTED: You Don't Need Acres for Quail"
**Publish Target:** May 15, 2026
**Resources:**
- [ ] Small space setup (balcony/garage corner)
- [ ] Urban quail keeper interview
- [ ] Cost breakdown graphics

---

## 📊 GitHub Traffic & Monetization

### Can You Monetize GitHub Traffic?
**Direct:** No — GitHub doesn't have an ad program
**Indirect:** Yes — several paths:

1. **GitHub Sponsors** — fans can sponsor your work
2. **Link to external monetization:**
   - YouTube videos (ad revenue)
   - Buy Me a Coffee / Ko-fi
   - Affiliate links in README
   - Sponsored content (disclosed)
   - Paid documentation/courses

3. **Open Source Business Models:**
   - Dual licensing (free OSS / paid commercial)
   - Support contracts
   - Hosted SaaS version
   - Consulting services

### Strategy for OpenClaw WebUI
- Open source on GitHub (builds community)
- README links to YouTube demos (drives views)
- YouTube description links back to GitHub (stars)
- GitHub Sponsors for ongoing development
- Consulting for custom deployments

**Flywheel:** GitHub stars → credibility → YouTube views → more users → sponsors

---

### Timeline
- **Eggs in incubator:** NOW
- **Expected hatch:** April 8-9, 2026 (10-11 days from Mar 29)
- **Video shoot window:** April 8-12 (hatch + first 48 hours)

### Research: Viral Bird Hatching Content

**Top Performing Formats:**

| Format | Example | Why It Works |
|--------|---------|--------------|
| **Contrast/Scale** | "World's Biggest vs Smallest Egg" (72M views) | Drama, curiosity, educational |
| **Rescue/Found Egg** | @fathenfarms button quail hatching (4M likes) | Emotional hook, underdog story |
| **Time-lapse Hatching** | A Chick Called Albert series (21M+ views) | Satisfying, miracle of life |
| **First Peep Moments** | @ducks_in_space "Hatching in Hand" (55K likes) | Intimate, immediate gratification |
| **Supermarket Egg** | Albert origin story (21M views, 2016) | Relatable, "anyone can do this" |

**Quail-Specific Opportunities:**
- Button quail = viral on TikTok (@fathenfarms 2.3M followers, 159M likes)
- Tiny size = adorable factor amplified
- Fast hatch (16-18 days) = content velocity
- Coturnix quail slightly larger, more robust for filming

**Key Elements for Virality:**
1. **Pipping moment** — first crack, struggle, breakthrough
2. **First fluff** — wet to dry transformation
3. **First steps** — wobbly, determined
4. **Sound** — peeping, cheeping (ASMR-like)
5. **Story arc** — beginning (egg) → conflict (hatch struggle) → resolution (fluffy chick)

### Shot List for April 8-12
- [ ] Day-before candling (veins visible, movement)
- [ ] Pipping start (first crack)
- [ ] Zipping phase (crack around egg)
- [ ] Full emergence (wet chick)
- [ ] Drying fluff transformation (time-lapse)
- [ ] First steps / first peep
- [ ] Sibling interactions (if multiple hatch)
- [ ] Feeding/water firsts

### Content Angles to Test
1. **"Day in the life of a hatching egg"** — 24hr time-lapse
2. **"Will they hatch?"** — suspense build with candling updates
3. **"The tiniest dinosaurs"** — quail specific, button quail angle
4. **"From egg to fluff in 60 seconds"** — condensed hatching
5. **"Supermarket egg challenge"** — if store-bought, relatable hook

### Technical Requirements
- Vertical 9:16 format (1080x1920)
- 30 seconds for Shorts/TikTok
- Macro lens for egg details
- Good lighting for candling shots
- Clean audio for peeping (or music overlay)

### Distribution
- **YouTube Shorts** — longer shelf life, searchable
- **TikTok** — faster virality, algorithm-driven
- **Cross-post** — maximize reach

**Next Action:** Scout shot locations, test macro setup, prep incubation log for candling footage.

---

## Recently Completed

- [x] Telegram voice message transcription (Whisper)
- [x] Mac audio announcement system (`say` integration)
- [x] Daily report cron job (LaunchAgent)
- [x] Daily-brief Flask service prototype
- [x] **Daily Report Reliability Enhancement** — Added retry logic (3 attempts) and Telegram failure alerts after Mail.app timeout caused missing report on 2026-03-30
  - **File:** `~/.openclaw/scripts/generate_daily_report.sh`
  - **Issue:** MailStorageManager high CPU caused AppleEvent timeout (-1712)
  - **Solution:** Exponential backoff (30s→60s→120s) + Telegram notification on final failure

