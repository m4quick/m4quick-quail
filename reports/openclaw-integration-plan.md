# OpenClaw Integration Plan
**Project:** Replace Alexa with OpenClaw-controlled voice assistant
**Date:** March 25, 2026
**Status:** Planning Phase

## Vision
Replace Amazon Alexa cloud dependency with:
- **Offline voice control** (Rhasspy/OpenWakeWord)
- **Self-hosted smart home** (Home Assistant)
- **Pi 4 as central hub** (Pi-hole + Home Assistant + Rhasspy)
- **Repurposed Echo hardware** (speakers/mic arrays)

## Architecture

### Current State (Alexa Cloud)
```
Voice → Amazon Cloud → Alexa Service → Smart Devices
                ↓
         Tracking/Ads
```

### Target State (OpenClaw Local)
```
Voice → Echo Hardware → Pi 4 (Rhasspy) → Home Assistant → Devices
                ↓
         Pi-hole (blocking)
```

### System Components

#### 1. Pi 4 (Central Hub) ✅ DEPLOYED
| Service | Purpose | Status |
|---------|---------|--------|
| Pi-hole | DNS filtering, ad blocking | ✅ Active |
| Docker | Container management | ✅ Active |
| DHCP | IP assignment | ✅ Native isc-dhcp-server |

#### 2. Rhasspy (Voice Assistant) - PLANNED
| Component | Function |
|-----------|----------|
| OpenWakeWord | Wake word detection ("Hey OpenClaw") |
| Whisper/Coqui | Speech-to-text (offline) |
| Mycroft/Piper | Text-to-speech (offline) |
| Home Assistant | Intent handling, actions |

#### 3. Home Assistant (Smart Home) - PLANNED
| Feature | Purpose |
|---------|---------|
| Device Integration | Control lights, switches, sensors |
| Automation | Time-based, event-based rules |
| Voice Integration | Rhasspy webhook triggers |
| Dashboard | Web UI for control |

#### 4. Echo Hardware (Repurposed) - IN PROGRESS
| Device | Current | Target |
|--------|---------|--------|
| Echo Dot Gen 3 | Amazon Alexa | Rhasspy speaker/mic |
| Google Home Mini | Google Assistant | TBD |

## Implementation Phases

### Phase 1: Infrastructure ✅ COMPLETE
**Status:** Done March 24-25, 2026
- ✅ Pi 4 with Raspberry Pi OS
- ✅ Pi-hole DNS filtering
- ✅ Native DHCP server
- ✅ Network migration

### Phase 2: Home Assistant - PRIORITY
**Timeline:** Week 1
**Tasks:**
- [ ] Install Home Assistant (Docker or HA OS)
- [ ] Integrate existing smart devices
- [ ] Configure dashboard
- [ ] Test device control

**Installation Options:**
```bash
# Docker (recommended for existing Pi)
docker run -d --name homeassistant \
  --privileged --restart=unless-stopped \
  -e TZ=America/New_York \
  -v /home/pi/homeassistant:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

**Access:** http://192.168.1.57:8123

### Phase 3: Rhasspy Voice Control
**Timeline:** Week 2
**Tasks:**
- [ ] Install Rhasspy (Docker)
- [ ] Configure wake word ("Hey OpenClaw")
- [ ] Train voice commands
- [ ] Integrate with Home Assistant

**Installation:**
```bash
docker run -d --name rhasspy \
  --restart-unless-stopped \
  -p 12101:12101 \
  -v /home/pi/rhasspy:/profiles \
  --device /dev/snd:/dev/snd \
  rhasspy/rhasspy:latest \
  --user-profiles /profiles \
  --profile en
```

**Access:** http://192.168.1.57:12101

### Phase 4: Echo Hardware Modification
**Timeline:** Week 3-4
**Tasks:**
- [ ] Research Gen 3 jailbreak (current)
- [ ] Attempt root access
- [ ] OR use as AUX peripheral
- [ ] Integrate speakers/mic with Rhasspy

**Options:**
| Option | Difficulty | Result |
|--------|-----------|--------|
| Jailbreak | Hard | Full Linux control |
| AUX Out | Easy | Speaker only |
| Replace Internals | Medium | Custom Pi inside |

### Phase 5: Testing & Refinement
**Timeline:** Week 5+
**Tasks:**
- [ ] Test all voice commands
- [ ] Compare functionality to Alexa
- [ ] Add missing features
- [ ] Family acceptance testing
- [ ] Document usage

## Required Commands

### Music Streaming (Replace Amazon Music)
| Command | Target |
|---------|--------|
| "Play music" | Local library (Navidrome/Jellyfin) |
| "Play jazz" | Spotify Connect API |
| "Play radio" | Internet radio streams |
| "Next song" | Media player controls |

### Smart Home Control
| Command | Action |
|---------|--------|
| "Turn on lights" | Home Assistant → Lights |
| "Set temperature to 72" | Thermostat control |
| "Is the door locked?" | Sensor status |
| "Goodnight" | Scene: lights off, locks on |

### Information (Replace Alexa Knowledge)
| Command | Source |
|---------|--------|
| "What's the weather?" | Local API (OpenWeatherMap) |
| "What time is it?" | System clock |
| "Set timer for 5 minutes" | Home Assistant timer |
| "Add eggs to shopping list" | Local database |

## Hardware Shopping List

### For Echo Modification
| Item | Purpose | Est. Cost |
|------|---------|-----------|
| USB-to-TTL Adapter | Serial access | $8 |
| Soldering Kit | PCB connections | $40 |
| Pogo Pins | Non-destructive test | $10 |
| Spudger Set | Case opening | $12 |

### For Voice Enhancement
| Item | Purpose | Est. Cost |
|------|---------|-----------|
| USB Microphone | Better voice pickup | $25 |
| Respeaker HAT | Pi audio + mic array | $60 |
| Powered Speakers | Audio output | $50 |

### For Smart Home
| Item | Purpose | Est. Cost |
|------|---------|-----------|
| Zigbee USB Stick | Device connectivity | $25 |
| Smart Plugs | Test devices | $30 |
| Motion Sensors | Automation triggers | $40 |

**Total Estimated:** $200-300 for full setup

## Risk Assessment

### Technical Risks
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Echo jailbreak fails | Medium | Use AUX fallback |
| Rhasspy accuracy low | Medium | Train custom models |
| Family resistance | High | Maintain Alexa parallel |

### Privacy Benefits
| Aspect | Before (Alexa) | After (OpenClaw) |
|--------|---------------|------------------|
| Voice Data | Amazon cloud | Local only |
| Command History | Stored forever | Configurable |
| Third Parties | Multiple vendors | Self-hosted |
| Network Traffic | Always online | Can be offline |

## Success Metrics

### Functionality Parity
- [ ] 90% of Alexa commands work
- [ ] Music streaming functional
- [ ] All smart devices controllable
- [ ] Information queries answered

### Privacy Goals
- [ ] Zero cloud voice processing
- [ ] No Amazon/Google data collection
- [ ] Local DNS blocking (Pi-hole)
- [ ] Audit trail of all network requests

### Acceptance Criteria
- [ ] Family uses OpenClaw daily
- [ ] No regression to Alexa for basic tasks
- [ ] New capabilities (custom commands)
- [ ] Documentation complete

## Next Actions (Tomorrow)
1. **Research Echo Gen 3 jailbreak** (detailed guide)
2. **Install Home Assistant** on Pi 4
3. **Test Home Assistant** with existing devices
4. **Plan Rhasspy integration**
5. **Order hardware** if needed

## Documentation
- **Pi-hole:** http://192.168.1.57/admin
- **Future Home Assistant:** http://192.168.1.57:8123
- **Future Rhasspy:** http://192.168.1.57:12101

---
**Prepared:** March 25, 2026
**Next Review:** After Phase 1 (Home Assistant install)
