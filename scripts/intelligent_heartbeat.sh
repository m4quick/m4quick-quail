#!/bin/bash
# Intelligent Heartbeat - Phase 1.1
# Only alerts on state changes or urgent issues

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
STATE_FILE="${WORKSPACE}/memory/heartbeat-state.json"
LOG_FILE="/tmp/intelligent_heartbeat.log"

# Colors for terminal output (not used in alerts, just logging)
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Load state
load_state() {
    if [[ -f "$STATE_FILE" ]]; then
        cat "$STATE_FILE"
    else
        echo '{}'
    fi
}

# Save state
save_state() {
    local new_state="$1"
    echo "$new_state" > "$STATE_FILE"
}

# Get value from JSON (simple, no external deps)
json_get() {
    local json="$1"
    local key="$2"
    echo "$json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('$key', 'null'))"
}

# Check if currently in quiet hours
is_quiet_hours() {
    local hour=$(date +%H)
    if [[ $hour -ge 23 || $hour -lt 8 ]]; then
        return 0
    fi
    return 1
}

# === CHECKS ===

check_disk() {
    local usage=$(df ~ | tail -1 | awk '{print $5}' | tr -d '%')
    echo "$usage"
}

check_memory() {
    local pressure=$(memory_pressure 2>/dev/null | grep "free percentage" | awk '{print $NF}' | tr -d '%' || echo "0")
    if [[ "$pressure" -lt 20 ]]; then
        echo "critical"
    elif [[ "$pressure" -lt 50 ]]; then
        echo "warning"
    else
        echo "normal"
    fi
}

check_pihole() {
    # SSH to Pi and check container
    local status=$(ssh -o ConnectTimeout=5 pi@192.168.1.57 'sudo docker inspect --format="{{.State.Status}}" pihole 2>/dev/null' || echo "unreachable")
    echo "$status"
}

check_n8n() {
    local status=$(docker inspect --format='{{.State.Status}}' n8n 2>/dev/null || echo "not_running")
    echo "$status"
}

# === INTELLIGENT ALERT LOGIC ===

STATE=$(load_state)
ALERTS=""

# Check Disk
CURRENT_DISK=$(check_disk)
LAST_DISK=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('lastStates', {}).get('disk_usage_percent', 0))")

if [[ "$CURRENT_DISK" -ge 90 ]]; then
    if [[ $(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print('true' if not d.get('alertsSent',{}).get('disk_critical') else 'false')") == "true" ]]; then
        ALERTS+="🚨 CRITICAL: Disk usage at ${CURRENT_DISK}% (threshold: 90%)\n"
        STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['alertsSent']['disk_critical']=True; print(json.dumps(d))")
    fi
elif [[ "$CURRENT_DISK" -ge 80 ]]; then
    if [[ $(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print('true' if not d.get('alertsSent',{}).get('disk_warning') else 'false')") == "true" ]]; then
        ALERTS+="⚠️ WARNING: Disk usage at ${CURRENT_DISK}% (threshold: 80%)\n"
        STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['alertsSent']['disk_warning']=True; print(json.dumps(d))")
    fi
else
    # Reset alert flags if back to normal
    if [[ "$LAST_DISK" -ge 80 && "$CURRENT_DISK" -lt 80 ]]; then
        ALERTS+="✅ Disk usage recovered: ${CURRENT_DISK}%\n"
    fi
    STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['alertsSent']['disk_warning']=False; d['alertsSent']['disk_critical']=False; print(json.dumps(d))")
fi

STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['lastStates']['disk_usage_percent']=$CURRENT_DISK; print(json.dumps(d))")

# Check Pi-hole
CURRENT_PIHOLE=$(check_pihole)
LAST_PIHOLE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('lastStates', {}).get('pihole', {}).get('status', 'unknown'))")

if [[ "$CURRENT_PIHOLE" != "running" ]]; then
    if [[ "$LAST_PIHOLE" == "running" || $(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print('true' if not d.get('alertsSent',{}).get('pihole_down') else 'false')") == "true" ]]; then
        ALERTS+="🚨 Pi-hole container is DOWN (status: $CURRENT_PIHOLE)\n"
        STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['alertsSent']['pihole_down']=True; print(json.dumps(d))")
    fi
else
    if [[ "$LAST_PIHOLE" != "running" ]]; then
        ALERTS+="✅ Pi-hole container is back UP and running\n"
    fi
    STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['alertsSent']['pihole_down']=False; d['lastStates']['pihole']={'status':'running','healthy':True}; print(json.dumps(d))")
fi

# Check n8n
CURRENT_N8N=$(check_n8n)
if [[ "$CURRENT_N8N" != "running" ]]; then
    if [[ $(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('lastChecks',{}).get('n8n','null'))") != "down" ]]; then
        ALERTS+="⚠️ n8n container is not running (status: $CURRENT_N8N)\n"
    fi
    STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['lastChecks']['n8n']='down'; print(json.dumps(d))")
else
    if [[ $(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('lastChecks',{}).get('n8n','null'))") == "down" ]]; then
        ALERTS+="✅ n8n container is back UP\n"
    fi
    STATE=$(echo "$STATE" | python3 -c "import json,sys; d=json.load(sys.stdin); d['lastChecks']['n8n']='up'; print(json.dumps(d))")
fi

# Update timestamps
STATE=$(echo "$STATE" | python3 -c "import json,sys,time; d=json.load(sys.stdin); d['lastChecks']['pihole']=$(date +%s); d['lastChecks']['disk']=$(date +%s); d['lastChecks']['n8n']=$(date +%s); print(json.dumps(d))")

# Save state
save_state "$STATE"

# Output alerts (empty if nothing to report)
if [[ -n "$ALERTS" ]]; then
    echo -e "$ALERTS"
else
    echo "HEARTBEAT_OK"
fi
