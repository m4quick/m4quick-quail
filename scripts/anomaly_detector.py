#!/usr/bin/env python3
"""
Anomaly Detector - Phase 2.2
Detect unusual patterns and proactively alert

Usage:
    python3 scripts/anomaly_detector.py
    python3 scripts/anomaly_detector.py --check-all
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import statistics

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
TRENDS_FILE = MEMORY_DIR / "anomaly_trends.json"


def load_trends():
    """Load historical trend data."""
    if TRENDS_FILE.exists():
        with open(TRENDS_FILE) as f:
            return json.load(f)
    return {
        'disk_samples': [],
        'memory_samples': [],
        'pihole_query_rates': [],
        'last_check': None,
        'baselines': {}
    }


def save_trends(data):
    """Save trend data."""
    TRENDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRENDS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_current_metrics():
    """Get current system metrics."""
    metrics = {}
    
    # Disk usage
    try:
        df = subprocess.run("df ~ | tail -1 | awk '{print $5}' | tr -d '%'", 
                          shell=True, capture_output=True, text=True)
        metrics['disk_percent'] = int(df.stdout.strip())
    except:
        metrics['disk_percent'] = None
    
    # Memory free percent
    try:
        mem = subprocess.run("memory_pressure 2>/dev/null | grep 'free percentage' | awk '{print $NF}' | tr -d '%'",
                           shell=True, capture_output=True, text=True)
        metrics['memory_free'] = int(mem.stdout.strip()) if mem.stdout.strip() else 0
    except:
        metrics['memory_free'] = None
    
    # Load average
    try:
        load = subprocess.run("uptime | awk -F'load averages:' '{print $2}' | awk '{print $1}'",
                             shell=True, capture_output=True, text=True)
        metrics['load_1m'] = float(load.stdout.strip().replace(',', ''))
    except:
        metrics['load_1m'] = None
    
    # Timestamp
    metrics['timestamp'] = datetime.now().isoformat()
    
    return metrics


def detect_anomalies(current, trends):
    """Detect anomalies based on historical data."""
    alerts = []
    
    # Need at least 7 samples for baseline (1 week of daily checks)
    if len(trends.get('disk_samples', [])) < 7:
        # Just record, don't alert yet
        return alerts
    
    # Calculate baselines
    disk_history = [s['value'] for s in trends['disk_samples'][-30:]]  # Last 30
    disk_mean = statistics.mean(disk_history)
    disk_std = statistics.stdev(disk_history) if len(disk_history) > 1 else 0
    
    # Check disk spike
    if current['disk_percent'] is not None:
        # Sudden jump (more than 2 std dev or 5% in one day)
        if disk_std > 0:
            z_score = (current['disk_percent'] - disk_mean) / disk_std
            if z_score > 2.5:
                alerts.append({
                    'type': 'anomaly',
                    'severity': 'warning',
                    'subject': 'disk_usage',
                    'message': f"📊 Disk usage spike detected: {current['disk_percent']}% (normal: {disk_mean:.1f}% ± {disk_std:.1f}%)",
                    'suggestion': 'Run `du -sh ~/*/ | sort -hr | head -10` to find large directories'
                })
        
        # Rapid growth (compared to yesterday)
        if len(trends['disk_samples']) >= 2:
            yesterday = trends['disk_samples'][-1]['value']
            change = current['disk_percent'] - yesterday
            if change >= 5:
                alerts.append({
                    'type': 'rapid_change',
                    'severity': 'warning' if change < 10 else 'critical',
                    'subject': 'disk_usage',
                    'message': f"🚀 Disk usage jumped {change}% in 24h (now {current['disk_percent']}%)",
                    'suggestion': 'Check for large downloads, log files, or temp directories'
                })
    
    # Check memory pressure change
    if current['memory_free'] is not None:
        memory_history = [s['value'] for s in trends.get('memory_samples', [])[-7:]]
        if memory_history:
            avg_free = statistics.mean(memory_history)
            if current['memory_free'] < avg_free * 0.7:  # 30% drop
                alerts.append({
                    'type': 'anomaly',
                    'severity': 'warning',
                    'subject': 'memory',
                    'message': f"🧠 Memory pressure increased: {current['memory_free']}% free (avg: {avg_free:.0f}%)",
                    'suggestion': 'Check for runaway processes: `ps aux | sort -nk +4 | tail -5`'
                })
    
    return alerts


def record_sample(trends, metric_name, value):
    """Record a metric sample."""
    if metric_name not in trends:
        trends[metric_name] = []
    
    trends[metric_name].append({
        'timestamp': datetime.now().isoformat(),
        'value': value
    })
    
    # Keep only last 60 samples (2 months of daily checks)
    trends[metric_name] = trends[metric_name][-60:]


def check_proactive_alerts():
    """Check for time-based proactive alerts."""
    alerts = []
    
    # Check certificate expiration (if any)
    # Could check: ~/.ssh/*.pub, ~/certificates/, etc.
    
    # Check for scheduled events approaching
    # Could integrate with calendar
    
    # Check backup status (if configured)
    
    return alerts


def main():
    check_all = '--check-all' in sys.argv
    
    trends = load_trends()
    current = get_current_metrics()
    
    # Record current metrics
    if current['disk_percent'] is not None:
        record_sample(trends, 'disk_samples', current['disk_percent'])
    if current['memory_free'] is not None:
        record_sample(trends, 'memory_samples', current['memory_free'])
    if current['load_1m'] is not None:
        record_sample(trends, 'load_samples', current['load_1m'])
    
    trends['last_check'] = datetime.now().isoformat()
    
    # Detect anomalies
    alerts = detect_anomalies(current, trends)
    
    # Check proactive alerts
    if check_all:
        proactive = check_proactive_alerts()
        alerts.extend(proactive)
    
    # Save trends
    save_trends(trends)
    
    # Output
    if alerts:
        print(json.dumps({
            'status': 'anomalies_detected',
            'alerts': alerts,
            'current_metrics': current,
            'baseline_samples': len(trends.get('disk_samples', []))
        }, indent=2))
    else:
        print(json.dumps({
            'status': 'normal',
            'current_metrics': current,
            'baseline_samples': len(trends.get('disk_samples', []))
        }, indent=2))


if __name__ == '__main__':
    main()
