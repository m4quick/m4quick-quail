# Which OpenClaw Interface Should You Use?
## A Zero Trust Guide — Video Script Draft v1

---

### COLD OPEN (0:00-0:30)

**[VISUAL: Split screen showing four interfaces - Terminal, Web Browser, Telegram, Signal]**

**SIR (V/O):**
"You want to run AI locally. Great. But how do you actually TALK to it? Terminal? Web browser? Telegram? Each one has different privacy implications. And as someone who's spent 20 years in federal security, let me tell you — not all interfaces are created equal."

**[TITLE CARD: "Which OpenClaw Interface?"]**

---

### THE PROBLEM (0:30-1:30)

**[VISUAL: Sir at desk, talking directly]**

**SIR:**
"OpenClaw is local-first AI. Your data never leaves your machine — in theory. But here's the thing: the interface you choose determines who sees what."

**[VISUAL: Diagram showing data flows]**

**SIR:**
"Use the terminal? Everything stays local. Use Telegram? Your messages pass through Telegram's servers. Use the WebUI? It depends on whether you're on localhost or exposing it to the internet."

**[VISUAL: Quick cut to each interface]**

**SIR:**
"Today I'm breaking down all four OpenClaw interfaces from a Zero Trust perspective. What data leaks, what doesn't, and which one you should use for what."

---

### INTERFACE 1: TUI (Terminal UI) (1:30-3:30)

**[VISUAL: Screen recording of terminal, typing `openclaw-tui`]**

**SIR (V/O):**
"First up: the Terminal UI, or TUI. This is the purest form of OpenClaw."

**[VISUAL: Terminal window showing conversation]**

**SIR:**
"When you type in the terminal, here's what happens: your keystrokes go to OpenClaw running on your machine. That's it. No network. No third parties. No logs in someone else's cloud."

**[VISUAL: Simple diagram: You → Terminal → OpenClaw → Response]**

**SIR:**
"Privacy rating? Five stars. Attack surface? Minimal. If someone wants to see your OpenClaw conversations, they need physical access to your machine or root privileges."

**[VISUAL: Sir back on camera]**

**SIR:**
"But — and there's always a but — it's terminal-only. No file uploads. No voice messages. No mobile access. If you're away from your desk, you're disconnected from your AI."

**When to use TUI:**
- ✅ Sensitive work (passwords, personal data, security topics)
- ✅ Code review and technical tasks
- ✅ When you need maximum privacy

**When NOT to use TUI:**
- ❌ Mobile workflows
- ❌ File handling
- ❌ Voice input

---

### INTERFACE 2: Enhanced TUI (WebUI) (3:30-5:30)

**[VISUAL: Browser showing localhost:5001, OpenClaw WebUI interface]**

**SIR (V/O):**
"Next: the Enhanced TUI, or WebUI. This is what I use for 80% of my work."

**[VISUAL: WebUI demo - chat interface, file upload, image display]**

**SIR:**
"The WebUI runs on your local machine — localhost port 5001. That means your browser talks to OpenClaw on the same computer. Your data never touches the internet."

**[VISUAL: Diagram: You → Browser → localhost:5001 → OpenClaw → Response]**

**SIR:**
"But here's the critical detail: it ONLY stays local if you use localhost or 127.0.0.1. The second you access it via your local IP address — like 192.168.1.100:5001 — browsers treat it differently. Secure context requirements kick in. Some features get disabled."

**[VISUAL: Split screen showing localhost vs IP address in browser]**

**SIR:**
"So the rule is: bookmark `http://localhost:5001`. Don't use the IP unless you're on the same machine."

**WebUI Features:**
- ✅ File uploads (documents, images)
- ✅ Image analysis display
- ✅ Voice recording (with Whisper transcription)
- ✅ Session history
- ✅ Mobile access via Tailscale (optional, encrypted)

**Privacy considerations:**
- ⚠️ File uploads temporarily stored on disk (purged after processing)
- ⚠️ Browser history contains conversation snippets
- ✅ Still local-only if accessed via localhost

**When to use WebUI:**
- ✅ Daily productivity work
- ✅ File handling and image analysis
- ✅ When you need visual interface

**Pro tip:** "I run this in a dedicated browser profile with history disabled for extra paranoia."

---

### INTERFACE 3: Telegram (5:30-8:00)

**[VISUAL: Phone screen showing Telegram chat with Enki]**

**SIR (V/O):**
"Now we get to the external interfaces. Starting with Telegram."

**[VISUAL: Message flow diagram]**

**SIR:**
"When you send a message via Telegram, here's the chain: Your phone → Telegram's servers → OpenClaw Gateway → your Mac running OpenClaw → response back through Telegram."

**[VISUAL: Diagram with Telegram cloud highlighted]**

**SIR:**
"That means Telegram — the company — can technically see your messages. They're encrypted in transit, but not end-to-end encrypted by default. And they're stored on Telegram's servers."

**[VISUAL: Sir serious face]**

**SIR:**
"From a Zero Trust perspective, this is... acceptable for certain use cases, but not ideal. You're trusting Telegram as an intermediary."

**Telegram Pros:**
- ✅ Always available (mobile, desktop, web)
- ✅ Voice messages (transcribed locally via Whisper)
- ✅ Rich media (images, documents)
- ✅ Works from anywhere

**Telegram Cons:**
- ❌ Messages traverse third-party servers
- ❌ Phone number tied to identity
- ❌ Telegram can read messages (not E2E by default)
- ❌ Metadata logged (when, who, how often)

**When to use Telegram:**
- ✅ Quick questions on the go
- ✅ Voice notes when away from desk
- ✅ Non-sensitive tasks ("What's the weather?", "Summarize this document")

**When NOT to use Telegram:**
- ❌ Passwords or credentials
- ❌ Personal/medical information
- ❌ Confidential work topics
- ❌ Anything you'd be upset if leaked

**SIR:**
"I use Telegram for convenience — "Remind me to check the eggs" — but never for anything sensitive."

---

### INTERFACE 4: Signal (8:00-10:00)

**[VISUAL: Signal app interface]**

**SIR (V/O):**
"What if you want mobile access AND privacy? Enter Signal."

**[VISUAL: Diagram showing E2E encryption]**

**SIR:**
"Signal uses end-to-end encryption by default. That means even Signal's servers can't read your messages. Only your phone and the OpenClaw Gateway can decrypt them."

**[VISUAL: Technical diagram with lock icons]**

**SIR:**
"For OpenClaw, Signal integration is newer and requires specific setup. But if your Gateway supports it, this is the most private way to access OpenClaw remotely."

**Signal Pros:**
- ✅ End-to-end encryption
- ✅ Open source (auditable)
- ✅ Non-profit, not data mining
- ✅ Same rich features as Telegram

**Signal Cons:**
- ⚠️ Requires phone number (like Telegram)
- ⚠️ OpenClaw Signal integration may be less mature
- ⚠️ Smaller user base (fewer bot integrations)

**When to use Signal:**
- ✅ Remote access to sensitive AI conversations
- ✅ When you need mobile + privacy
- ✅ Federated contractor work (compliance requirements)

---

### THE DECISION MATRIX (10:00-11:30)

**[VISUAL: Full-screen comparison table]**

| Interface | Privacy | Convenience | Features | Best For |
|-----------|---------|-------------|----------|----------|
| **TUI** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | Sensitive work, coding |
| **WebUI** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Daily productivity |
| **Signal** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Private mobile access |
| **Telegram** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Convenience, non-sensitive |

**SIR:**
"Here's my personal setup: TUI for security-sensitive work. WebUI for 80% of daily tasks. Telegram for quick mobile questions. Signal if I need private remote access — though honestly, I rarely need that level of paranoia for AI conversations."

---

### THE ZERO TRUST PRINCIPLE (11:30-12:30)

**[VISUAL: Sir back on camera, serious tone]**

**SIR:**
"The Zero Trust mindset is simple: verify everything, trust nothing. When choosing an OpenClaw interface, ask yourself: who else can see this data?"

**[VISUAL: Text overlay with questions]**

**SIR:**
"With TUI, the answer is: nobody except you. With WebUI, it's: nobody if you use localhost. With Telegram, it's: Telegram, potentially law enforcement with warrants, and anyone who compromises Telegram's servers."

**[VISUAL: Sir more relaxed]**

**SIR:**
"That doesn't make Telegram evil. It makes it a trade-off. And understanding that trade-off is what Zero Trust is all about."

---

### CALL TO ACTION (12:30-13:00)

**[VISUAL: Split screen with all four interfaces]**

**SIR:**
"So which OpenClaw interface should YOU use? It depends on your threat model. For most people, the WebUI hits the sweet spot. Privacy-focused? Stick to TUI. Need mobile? Use Telegram knowingly. Need mobile AND privacy? Look into Signal."

**[VISUAL: Subscribe button, GitHub link]**

**SIR:**
"In the next video, I'm going to show you how to set up ALL four interfaces and configure them for maximum privacy. Subscribe and hit the bell so you don't miss it."

**[END CARD: "OpenClaw Security Series — Episode 2: Setting Up Your Interfaces"]**

---

## TECHNICAL NOTES

### B-Roll Needed:
- [ ] Screen recording: TUI in terminal
- [ ] Screen recording: WebUI on localhost:5001
- [ ] Phone screen: Telegram chat
- [ ] Phone screen: Signal chat
- [ ] Data flow diagrams (animated arrows showing path)
- [ ] Sir at desk, multiple takes with different expressions
- [ ] Close-up of Sir typing in terminal
- [ ] Split screen of all four interfaces

### Graphics Needed:
- [ ] Privacy comparison table (animated reveal)
- [ ] Data flow diagrams for each interface
- [ ] Zero Trust principle text overlay
- [ ] End card with subscribe/GitHub links

### Audio:
- [ ] Background music (tech/security theme, not too intense)
- [ ] Transition sounds for interface switches
- [ ] Emphasis sound when mentioning "privacy"

### Key Props:
- Laptop showing interfaces
- Phone showing Telegram/Signal
- Maybe a "privacy" visual metaphor (lock, shield)

---

## QUESTIONS FOR SIR

1. **Do you actually use Signal with OpenClaw**, or should I position this as "theoretical best option"?

2. **Tailscale mention:** Should I include Tailscale as a "bonus option" for remote WebUI access with encryption?

3. **Tone check:** Is this too paranoid, or just right for your "Zero Trust Architect" brand?

4. **Demo or explain:** Do you want to actually DEMONSTRATE sending a message through each interface, or keep it conceptual?

---

## RUNTIME TARGET

**Total:** 13 minutes  
**Format:** Talking head + screen recordings + graphics  
**Pacing:** Educational but engaging — not a lecture

---

**Status: DRAFT v1 — Ready for review**