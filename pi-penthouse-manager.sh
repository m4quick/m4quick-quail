#!/bin/bash
# Pi 4 Penthouse Manager
# Control Pi-hole + Voice Satellite from Mac

PI_HOST="pi-hole.local"  # Or Tailscale IP
PI_USER="pi"

echo "🥧 Enki Pi Manager - Penthouse"
echo "================================"
echo ""

check_pi() {
    if ping -c 1 -W 2 $PI_HOST &>/dev/null; then
        echo "✅ Pi online: $PI_HOST"
        return 0
    else
        echo "❌ Pi not reachable"
        return 1
    fi
}

show_menu() {
    echo ""
    echo "1) 🚀 First-time setup (SSH key)"
    echo "2) 📤 Copy setup script to Pi"
    echo "3) 🔧 Run full setup on Pi"
    echo "4) 📋 Edit config.json"
    echo "5) 🎤 Start voice service"
    echo "6) 🛑 Stop voice service"
    echo "7) 📊 Status"
    echo "8) 📜 View logs"
    echo "9) 🕳️ Pi-hole admin"
    echo "10) 🔄 Restart Pi"
    echo "11) 🔌 SSH to Pi"
    echo "q) Quit"
    echo ""
}

first_time() {
    read -p "Pi IP or hostname [pi-hole.local]: " addr
    PI_HOST=${addr:-pi-hole.local}
    echo "Copying SSH key..."
    ssh-copy-id $PI_USER@$PI_HOST
    echo "✅ Done - passwordless access enabled"
}

copy_script() {
    check_pi || return
    echo "📤 Copying setup script..."
    scp pi4-penthouse-setup.sh $PI_USER@$PI_HOST:/tmp/
    echo "✅ Copied to /tmp/pi4-penthouse-setup.sh"
}

run_setup() {
    check_pi || return
    echo "🔧 Running setup (15 minutes)..."
    ssh -t $PI_USER@$PI_HOST "sudo bash /tmp/pi4-penthouse-setup.sh"
}

edit_config() {
    check_pi || return
    echo "📋 Opening config.json..."
    echo "Values to set:"
    echo "  1. Get Mac Tailscale IP: tailscale status"
    echo "  2. Get OpenClaw token: grep token ~/.openclaw/openclaw.json"
    echo "  3. Get Picovoice key: https://console.picovoice.ai"
    echo ""
    ssh -t $PI_USER@$PI_HOST "sudo nano /home/pi/enki-voice/config.json"
}

start_voice() {
    check_pi || return
    ssh $PI_USER@$PI_HOST "sudo systemctl start enki-voice-penthouse"
    echo "✅ Voice service started"
}

stop_voice() {
    check_pi || return
    ssh $PI_USER@$PI_HOST "sudo systemctl stop enki-voice-penthouse"
    echo "✅ Voice service stopped"
}

check_status() {
    check_pi || return
    echo "📊 Voice service:"
    ssh $PI_USER@$PI_HOST "sudo systemctl status enki-voice-penthouse --no-pager | head -10"
    echo ""
    echo "📊 Pi-hole status:"
    ssh $PI_USER@$PI_HOST "pihole status"
}

view_logs() {
    check_pi || return
    echo "📜 Logs (Ctrl+C to exit):"
    ssh -t $PI_USER@$PI_HOST "sudo journalctl -u enki-voice-penthouse -f --since '1 hour ago'"
}

open_pihole() {
    PI_IP=$(ssh $PI_USER@$PI_HOST "hostname -I | awk '{print \$1}'")
    echo "🕳️ Opening Pi-hole admin..."
    echo "URL: http://$PI_IP/admin"
    open "http://$PI_IP/admin"
}

restart_pi() {
    check_pi || return
    ssh $PI_USER@$PI_HOST "sudo reboot"
    echo "⏳ Rebooting..."
}

ssh_pi() {
    check_pi || return
    ssh $PI_USER@$PI_HOST
}

# Main
while true; do
    show_menu
    read -p "Choice: " choice
    
    case $choice in
        1) first_time ;;
        2) copy_script ;;
        3) run_setup ;;
        4) edit_config ;;
        5) start_voice ;;
        6) stop_voice ;;
        7) check_status ;;
        8) view_logs ;;
        9) open_pihole ;;
        10) restart_pi ;;
        11) ssh_pi ;;
        q|Q) exit 0 ;;
        *) echo "❌ Invalid" ;;
    esac
    echo ""
    read -p "Press Enter..."
    clear
done
