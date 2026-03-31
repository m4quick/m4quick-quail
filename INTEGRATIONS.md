# INTEGRATIONS.md — Multi-Agent System Architecture

_How the tools connect and interact. Reference when adding new integrations._

## System Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   memU Bot  │◄───►│   n8n       │◄───►│   Enki      │
│  (Planning) │     │ (Scheduled) │     │  (Complex)  │
└─────────────┘     └──────┬──────┘     └──────┬──────┘
                           │                    │
                    ┌───────┴───────┐    ┌──────┴──────┐
                    │  Webhooks     │    │  File System │
                    │  Automations  │    │  Tools       │
                    └───────────────┘    └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │ Telegram│  │  Email  │  │  Alexa  │
        └─────────┘  └─────────┘  └─────────┘
```

## Agent Responsibilities

### memU Bot (Memory & Planning)
**Role:** Long-term memory, task tracking, scheduling decisions  
**Input:** Conversations, user directives  
**Output:** Plans, reminders, task assignments  
**Integration:** Ideally writes to shared files; currently hosted API (paid)

### n8n (Scheduled Execution)
**Role:** Trigger workflows on schedule or webhook  
**Input:** HTTP requests, time-based triggers  
**Output:** Executes actions, calls other services  
**Status:** Running on port 5678, up 6+ hours (contradicts "removed" claim)

### Enki / OpenClaw (Complex Tasks)
**Role:** Ad-hoc complex tasks requiring reasoning, tools, code  
**Input:** Telegram messages, voice, heartbeats  
**Output:** Actions, files, code, responses  
**Limitations:** Session-based (wakes fresh), no native task queue

---

## Communication Patterns

### 1. File-Based Sync (Preferred — Free)
**How:** Shared directory with markdown files  
**Status:** Not yet implemented  
**Blocker:** memU hosted API is paid; need local file write capability

**Proposed structure:**
```
/shared-memory/
  ├── tasks/
  │   ├── pending/
  │   ├── in-progress/
  │   └── completed/
  ├── context/
  │   ├── current-projects.md
   │   └── decisions.md
  └── notifications/
      └── urgent.md
```

### 2. Webhook Integration (Current)
**How:** HTTP POST to n8n or Flask services  
**Used by:** Daily-brief service  
**Endpoint:** `http://localhost:5000/generate`

### 3. Direct CLI Execution (Current)
**How:** Shell commands, file operations  
**Used by:** Himalaya email, report generation  
**Scope:** Local Mac only

---

## Data Flow Examples

### Daily Report Generation
```
LaunchAgent (8 AM) ──► Script ──► Report file
                                    │
                                    ▼
                              [Future: Email via Himalaya]
```

### User Request: "Check Pi-hole"
```
Telegram ──► Enki ──► SSH to Pi-hole ──► Reply with status
```

### Planned: Task Assignment
```
memU: "Create quail video script"
    │
    ├──► Writes to /shared-memory/tasks/pending/quail-video.md
    │
    └──► Enki reads file ──► Creates script ──► Updates status
```

---

## Integration Checklist

- [x] Telegram voice → Whisper transcription
- [x] Mac audio announcements (`say`)
- [x] Report generation → Local files
- [ ] Report generation → Email (pending password)
- [ ] memU → File sync (needs memU local mode)
- [ ] n8n → Enki webhook triggers
- [ ] Alexa → OpenClaw commands

## Key Files

| File | Purpose | Updated By |
|------|---------|------------|
| `PROJECTS.md` | Active work tracker | Enki |
| `SCHEDULE.md` | Recurring tasks | Enki |
| `TOOLS.md` | Environment specifics | Enki |
| `memory/YYYY-MM-DD.md` | Daily logs | Enki |
| `HEARTBEAT.md` | Periodic check list | Enki |

---

## Decision Log

**2026-03-29:** Sticking with file-based memory instead of memU paid API  
**Rationale:** Zero cost, local-first, no vendor lock-in

**2026-03-28:** Enki handles complex tasks; n8n handles scheduled; memU handles planning  
**Rationale:** Clear boundaries prevent overlap

