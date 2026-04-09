# GitHub Strategy & CI/CD Pipeline

**Organization:** `m4quick-studio` (GitHub Org)

## Repository Structure

### Private Repositories

| Repo | Purpose | Contents |
|------|---------|----------|
| `openclaw-scripts` | Daily automation | Daily Report, Daily Brief, health checks |
| `privacybox-config` | NUC infrastructure | Docker Compose, deployment scripts |
| `m4quick-internal` | Private planning | Notes, plans, non-public documentation |

### Public Repositories

| Repo | Purpose | Trigger for Public |
|------|---------|-------------------|
| `open-webui` | OpenClaw backend integration | 🆕 **Forked** — active development |
| `openclaw-webui` | (archived) | ⛔ Old approach — superseded |
| `openclaw-memory` | Memory system module | When stable, tested |

### Affiliate & Commerce

| Repo | Purpose | Contents |
|------|---------|----------|
| `m4quick-affiliates` | Amazon/AWS affiliate links | Product recommendations, link generators |

**Affiliate IDs:**
- Amazon Associates: `m4quickquail-20` (~4-10% commission)

**Tools:**
- `amazon-link.sh` — Generate affiliate links on demand
- `yt-affiliate.sh` — Create YouTube descriptions with tracking links

**Content:**
- Quail hatching equipment (incubators, feed, cages)
- Tech gear (cameras, NUC, Pi)
- Privacy/security tools

---

## Open WebUI + OpenClaw Integration Architecture

### Phase 1: Basic Backend (Now)
- OpenClaw Gateway as OpenAI-compatible backend
- WebUI manages its own chat history
- OpenClaw memory remains separate (file-based)

### Phase 2: Unified Memory (PrivacyBox)
**Goal:** Seamless memory bridge between WebUI and OpenClaw

```
┌─────────────────────────────────────────┐
│         Open WebUI Interface            │
│  ┌─────────┐      ┌──────────────┐   │
│  │  Chat   │─────▶│ Memory Bridge  │   │
│  │ History │◀─────│   (Python)     │   │
│  └─────────┘      └──────┬───────┘   │
└──────────────────────────┼───────────┘
                           │
           ┌───────────────▼───────────────┐
           │    Memory Sync Layer          │
           │  ┌─────────────────────────┐   │
           │  │  ~/.openclaw/memory/    │   │
           │  │  ├── webui/             │   │
           │  │  │   └── YYYY-MM-DD.md │   │
           │  │  ├── heartbeat/         │   │
           │  │  └── facts/             │   │
           │  └─────────────────────────┘   │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │      RAG Index              │
           │  (ChromaDB / Weaviate)      │
           └─────────────────────────────┘
```

**Sync Method: File Watcher (Event-Driven)**
- **Why:** Lowest overhead, fastest for local-first (PrivacyBox)
- **How:** WebUI writes to `memory/webui/`, OpenClaw watches with fsnotify/inotify
- **Latency:** ~10-100ms (event-driven, not polling)
- **Implementation:** Python `watchdog` library

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MemorySyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            update_memory_index(event.src_path)
            sync_to_openclaw_context(event.src_path)
```

**Benefits:**
- ✅ Zero network overhead (local filesystem)
- ✅ Aligns with OpenClaw's file-based architecture
- ✅ Near real-time sync
- ✅ Survives restarts (persistent files)

---

## CI/CD Pipeline Targets

### Stage 1: Source Control
Local development → Gitea (local) → Private GitHub → Public GitHub

### Stage 2: Automated Testing
- Shellcheck for scripts
- Docker build tests
- Integration tests

### Stage 3: Deployment
- Daily Report: cron → macOS LaunchAgent
- Daily Brief: Docker → NUC (PrivacyBox)
- Motion Detection: Systemd/n8n schedule
- Website: GitHub Pages or VPS

### Stage 4: Monitoring
- Health checks via heartbeat
- Log aggregation
- Alert on failure

## Pipeline Criteria

| Project | Pipeline Ready When |
|---------|---------------------|
| Daily Report | Working, needs versioning |
| Daily Brief | Flask app stable |
| PrivacyBox | Hardware received |
| Motion Detection | Tested, needs scheduling |
| Affiliate Links | Content curated, links tested |
| Open WebUI Fork | Backend integration working |

---

*2026-04-06: Documented M4Quick Studios org structure, archived old repo, forked Open WebUI, defined memory sync architecture*  
*Next: Implement OpenClaw backend in fork, test memory bridge*
