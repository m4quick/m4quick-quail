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
  - DHCP: Built-in (active), range 192.168.1.101-200
  - Monitor: /usr/local/bin/pihole-dhcp-monitor.sh (every 5 min)
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

Add whatever helps you do your job. This is your cheat sheet.
