# ChickAi Guardian Mode - Feature Specification

## Overview
Location-aware monitoring that activates when keeper leaves incubator proximity. Smart alerts based on absence duration and chick development stage.

## Core Concept
**"ChickAi watches so you don't miss the magic. But you still have to do the work."**

Guardian Mode is a safety net, not a replacement for care. It ensures critical hatching moments aren't missed during brief absences.

---

## Activation Triggers

### Primary: Bluetooth Proximity
- BLE beacon in/on incubator (~$5 cost)
- Phone app monitors signal strength (RSSI)
- Trigger: Signal lost for >grace period

### Secondary: Manual Activation
- User manually enables before leaving
- Overrides proximity detection
- Useful for: Phone left home, Bluetooth off

### Tertiary: Time-Based (Scheduled)
- Pre-scheduled work hours
- Recurring: M-F 9AM-5PM
- One-time: "Grocery run - 2 hours"

---

## Grace Period Settings

| Duration | Use Case | Default Alerts |
|----------|----------|----------------|
| 5 minutes | Quick errands | Level 2+ only |
| 15 minutes | Gym, coffee | Level 2+ only |
| 30 minutes | Shopping, meetings | Level 1+ |
| 2 hours | Work commute | All levels |
| 8 hours | Full work day | All levels |

**Custom:** User-defined minutes (5-480)

---

## Alert Levels & Escalation

### Level 1: Activity Detected (Info)
- **Trigger:** Motion in incubator
- **Message:** "Activity in incubator - all normal"
- **Delivery:** App notification (silent)
- **Frequency:** Max 1 per hour

### Level 2: Development Milestone (Alert)
- **Trigger:** Pipping detected, egg rolling, vocalization
- **Message:** "🐣 PIPPING DETECTED - Hatch may start soon!"
- **Delivery:** Push notification + SMS
- **Action:** Recommend returning within 2 hours

### Level 3: Critical Event (URGENT)
- **Trigger:** First hatch, multiple hatches, distress signals
- **Message:** "🚨 FIRST HATCH! Chicks need you NOW!"
- **Delivery:** Push + SMS + Phone call
- **Action:** Immediate return required

---

## Distance Thresholds

| Range | Bluetooth Signal | Use Case |
|-------|------------------|----------|
| 10 ft | Strong (-40 dBm) | Same room, quick tasks |
| 50 ft | Medium (-60 dBm) | House, yard work |
| 200 ft | Weak (-80 dBm) | Property, neighborhood |
| Custom | User-defined | Specific needs |

**Note:** Bluetooth range varies by environment (walls, interference)

---

## VACATION MODE (Advanced/Edge Case)

### ⚠️ CRITICAL WARNINGS

```
┌─────────────────────────────────────────┐
│  ⚠️ VACATION MODE - HIGH RISK ⚠️       │
│                                         │
│  Chicks require DAILY:                  │
│  • Feeding (multiple times/day)         │
│  • Fresh water                          │
│  • Brooder cleaning                     │
│  • Temperature monitoring                 │
│                                         │
│  Extended absence = HIGH MORTALITY RISK │
│                                         │
│  Enable ONLY if:                        │
│  ✓ Automated feeder/waterer installed    │
│  ✓ Emergency contact configured          │
│  ✓ Backup camera system active           │
│  ✓ Experienced keeper status             │
│                                         │
│  [ ] I understand the risks            │
│  [ ] Emergency contact confirmed         │
│  [ ] Automated systems tested            │
│                                         │
│  [ Enable - 48hr max ] [ Cancel ]       │
└─────────────────────────────────────────┘
```

### Requirements for Vacation Mode
1. **Automated feeder** with 3+ day capacity
2. **Water system** (multiple sources, no-spill)
3. **Backup camera** (redundant monitoring)
4. **Emergency contact** (local person who can intervene)
5. **Temperature alerts** (brooder failure = death)
6. **48-hour maximum** (hard limit)

### Marketing Position
- **Feature exists** for edge cases
- **Not promoted** as primary use case
- **Advanced users only** with full automation
- **Beginner warning:** "Not recommended for first-time keepers"

---

## Quiet Hours

**Default:** 11:00 PM - 6:00 AM

| Alert Level | Quiet Hours Behavior |
|-------------|---------------------|
| Level 1 | Silenced (logged only) |
| Level 2 | Push only (no SMS/call) |
| Level 3 | All methods (emergency override) |

**Customizable:** User sets quiet window

---

## UI/UX Design

### Guardian Status Indicator
```
┌────────────────────────────┐
│ 🛡️ Guardian Mode: ACTIVE   │
│                             │
│ Proximity: ●○○○ 50ft away   │
│ Grace: 12 min remaining     │
│ Alerts: Level 2+ enabled    │
│                             │
│ Last check: 2 min ago ✓     │
│ Next check: 3 min           │
└────────────────────────────┘
```

### Activation Flow
1. User leaves Bluetooth range
2. Grace period countdown begins (visual + audio)
3. Grace expires → Guardian Mode activates
4. Monitoring intensifies (more frequent checks)
5. Alerts trigger based on events
6. User returns → proximity detected → auto-deactivate

### Deactivation
- **Automatic:** Phone returns to range
- **Manual:** User disables in app
- **Scheduled:** Time window expires

---

## Technical Implementation

### Bluetooth Beacon
- **Hardware:** iBeacon/Eddystone compatible ($3-10)
- **Battery:** CR2032, 1-2 year life
- **Range:** 10-100m depending on environment
- **ID:** Unique UUID per incubator

### Phone App
- **Background monitoring:** iOS/Android location services
- **Battery impact:** Minimal (<5% per day)
- **Offline handling:** Queue alerts, send when online

### Server Component
- **Status tracking:** Guardian state per user
- **Alert routing:** Push/SMS/call via Twilio
- **Escalation logic:** Time-based + event-based

---

## Pricing Strategy

### Free Tier
- Basic motion alerts (always on)
- Manual Guardian activation
- 15-minute grace period only

### Pro Tier ($9.99/mo or $99/yr)
- Bluetooth proximity detection
- Custom grace periods (5min - 8hrs)
- All alert levels with escalation
- Quiet hours configuration
- SMS + phone call alerts
- Vacation Mode (with warnings)

### Enterprise (Farms)
- Multiple incubators
- Staff notification routing
- Integration with farm management systems

---

## Safety & Ethics

### Product Responsibility
- **Never market as:** "Leave your chicks unattended!"
- **Always emphasize:** "Safety net, not replacement for care"
- **Education:** Link to chick care best practices
- **Community:** Forum for responsible keeping

### Legal Considerations
- **Terms of Service:** User acknowledges care requirements
- **Liability:** ChickAi monitors but doesn't care for animals
- **Local laws:** Some areas require animal welfare checks

---

## Future Enhancements

### Phase 2
- **Smartwatch integration:** Apple Watch, Wear OS alerts
- **Home automation:** Connect to smart feeders/waterers
- **AI prediction:** "Hatch likely in next 4 hours" warnings

### Phase 3
- **Community features:** "Neighbor network" - nearby keepers who can help
- **Vet integration:** Emergency vet contact in app
- **Insurance:** Partner with pet/livestock insurance

---

## Success Metrics

- **Activation rate:** % of users who enable Guardian Mode
- **Alert accuracy:** False positive rate (target: <5%)
- **Response time:** Average time to return after Level 3 alert
- **User satisfaction:** NPS score for Pro tier
- **Safety record:** Zero incidents of neglect via app

---

**Last Updated:** 2026-04-09
**Status:** Specification complete, ready for implementation
**Priority:** High (differentiating feature)
