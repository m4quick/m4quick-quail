#!/bin/bash
# Pi-hole Block Monitor
# Run on Pi: ssh pi@192.168.1.57 "bash /tmp/pihole_monitor.sh"

LOG="/tmp/pihole_monitor.log"
echo "=== Pi-hole Monitor Started: $(date) ===" > $LOG

while true; do
    # Check last 5 minutes of blocked queries
    BLOCKED=$(sudo docker logs pihole --since 5m 2>/dev/null | grep -c "gravity blocked\|regex blocked" || echo 0)
    TOTAL=$(sudo docker logs pihole --since 5m 2>/dev/null | grep -c "query\[A" || echo 0)
    
    echo "$(date): Blocked: $BLOCKED / Total: $TOTAL" >> $LOG
    
    # Alert if >20 blocks per 5min from same device
    if [ $BLOCKED -gt 20 ]; then
        echo "⚠️ HIGH BLOCKING: $BLOCKED queries blocked in 5 minutes" >> $LOG
        sudo docker logs pihole --since 5m 2>/dev/null | grep "blocked" | tail -10 >> $LOG
    fi
    
    sleep 300
done
