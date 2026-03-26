# HEARTBEAT.md - Periodic Checks

## Network Infrastructure (2x daily)
- [ ] Check Pi-hole DNS service responding
- [ ] Check DHCP server status (isc-dhcp-server)
- [ ] Verify Alexa devices have active leases
- [ ] Check for excessive blocked queries (potential issues)

## Daily Brief (8 AM ET)
- Email summary
- Calendar events
- Weather forecast
- Burn rate / AI costs
- System status (disk, updates)
- Network health (Pi-hole, DHCP, devices)
- Project updates

## Action Items
- If DHCP down → Restart via SSH: `sudo systemctl restart isc-dhcp-server`
- If Pi-hole blocking critical services → Whitelist domains
- If Alexa offline → Check DHCP lease expiration
- Report any issues immediately

## Pi-hole Access
- IP: 192.168.1.57
- SSH: pi@192.168.1.57 (Docker container: pihole)
- Web admin: http://192.168.1.57/admin
