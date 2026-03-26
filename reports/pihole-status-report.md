# Pi-hole Network Status Report
**Generated:** March 25, 2026, 12:22 AM

## System Overview
| Component | Status | Details |
|-----------|--------|---------|
| Pi-hole DNS | ✅ Active | Port 53, 86,064 blocked domains |
| Pi-hole Web | ✅ Accessible | http://192.168.1.57/admin |
| DHCP Server | ✅ Active | Native isc-dhcp-server, port 67 |
| Pi 4 Static IP | ✅ Reserved | 192.168.1.57 (MAC: dc:a6:32:0e:0d:95) |
| Router DHCP | ❌ Disabled | Netgear C7000v2 |

## Network Configuration
- **Gateway:** 192.168.1.1
- **DNS Server:** 192.168.1.57 (Pi-hole)
- **DHCP Range:** 192.168.1.101 - 192.168.1.200
- **Subnet Mask:** 255.255.255.0

## Active Blocklists
1. **StevenBlack Unified Hosts** - 86,064 domains
   - Ads, trackers, malware
   - ✅ Safe for music streaming
   - ✅ Alexa/Google voice services not blocked

## Connected Devices

| Device | IP Address | MAC Address | Status | Notes |
|--------|-----------|-------------|--------|-------|
| MichaelacStudio (Mac) | 192.168.1.101 | 1c:1d:d3:e5:8d:e9 | ✅ Active | Primary workstation |
| Apple Watch | 192.168.1.102 | ee:a7:0f:b6:21:6d | ✅ Active | Test device |
| Google-Home-Mini | 192.168.1.103 | 20:df:b9:b9:ed:b2 | ✅ Active | Renewed DHCP lease |
| Office Alexa (Gen 3) | 192.168.1.104 | 1c:fe:2b:1e:64:56 | ✅ Active | Music streaming tested, working |

## Music Streaming Status
| Service | Domain | Status | Blocked |
|---------|--------|--------|---------|
| Amazon Music | dss-na.amazon.com | ✅ Working | No |
| Alexa Voice | Various Amazon domains | ✅ Working | No |
| Weather API | amazon.com subdomains | ✅ Working | No |

## Pending Actions
- [ ] Test Google Home Mini music streaming
- [ ] Add remaining Alexa devices to Pi-hole network
- [ ] Evaluate aggressive blocklists (caution: may break streaming)
- [ ] Document any whitelist needs

## Access Credentials
- **Pi-hole Admin:** http://192.168.1.57/admin
- **Password:** Ver!zon723640695
- **SSH:** pi@192.168.1.57

## Troubleshooting Notes
- If device can't connect: Forget WiFi → Reconnect
- If music stops: Check Query Log for blocked domains
- Conservative blocklist keeps streaming services functional
