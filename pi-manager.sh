#!/bin/bash
# Enki Pi Manager
# Control the Raspberry Pi voice satellite from Mac

PI_HOST="pi-voice.local"  # Or use Tailscale IP: 100.x.x.x
PI_USER="pi"
PI_DIR="/home/pi/enki-voice"

echo "🥧 Enki Pi 4 Voice Satellite Manager"
echo "====================================="
echo ""

# Check if Pi is reachable
check_pi() {
    if ping -c 1 -W 2 $PI_HOST &>/dev/null; then
        echo "✅ Pi is online at $PI_HOST"
        return 0
    else
        echo "❌ Pi is not reachable at $PI_HOST"
        echo "   Check: Is Pi powered on? Same network?"
        return 1
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "Options:"
    echo "1) 🚀 Setup Pi (first time)"
    echo "2) 📤 Copy setup script to Pi"
    echo "3) 🔧 Run setup on Pi"
    echo "4) 🎤 Start voice service"
    echo "5) 🛑 Stop voice service"
    echo "6) 📊 Check service status"
    echo "7) 📜 View service logs"
    echo "8) 🔌 SSH into Pi"
    echo "9) 🔄 Restart Pi"
    echo "10) 🏠 Back to menu"
    echo "q) ❌ Quit"
    echo ""
}

setup_pi_first_time() {
    echo "Setting up Pi for first time..."
    echo ""
    echo "Prerequisites:"
    echo "- Pi must have Raspberry Pi OS Lite installed"
    echo "- Pi must be on same network as this Mac"
    echo "- You know Pi's IP or hostname (pi-voice.local)"
    echo ""
    read -p "Enter Pi IP or hostname [pi-voice.local]: " pi_addr
    PI_HOST=${pi_addr:-pi-voice.local}
    
    echo ""
    echo "Copying SSH key for passwordless access..."
    ssh-copy-id $PI_USER@$PI_HOST
    
    echo ""
    echo "✅ SSH key copied! You can now manage Pi without password."
}

copy_script() {
    if ! check_pi; then return; fi
    
    echo "📤 Copying setup script to Pi..."
    scp pi4-setup.sh $PI_USER@$PI_HOST:/tmp/
    echo "✅ Script copied to /tmp/pi4-setup.sh"
}

run_setup() {
    if ! check_pi; then return; fi
    
    echo "🔧 Running setup on Pi..."
    echo "   (This will take 10-15 minutes)"
    echo ""
    ssh -t $PI_USER@$PI_HOST "bash /tmp/pi4-setup.sh"
}

start_voice() {
    if ! check_pi; then return; fi
    
    echo "🎤 Starting voice service..."
    ssh $PI_USER@$PI_HOST "sudo systemctl start enki-voice"
    echo "✅ Voice service started"
}

stop_voice() {
    if ! check_pi; then return; fi
    
    echo "🛑 Stopping voice service..."
    ssh $PI_USER@$PI_HOST "sudo systemctl stop enki-voice"
    echo "✅ Voice service stopped"
}

check_status() {
    if ! check_pi; then return; fi
    
    echo "📊 Service status:"
    ssh $PI_USER@$PI_HOST "sudo systemctl status enki-voice --no-pager"
}

view_logs() {
    if ! check_pi; then return; fi
    
    echo "📜 Recent logs (Ctrl+C to exit):"
    ssh -t $PI_USER@$PI_HOST "sudo journalctl -u enki-voice -f --since '1 hour ago'"
}

ssh_into_pi() {
    if ! check_pi; then return; fi
    
    echo "🔌 Connecting to Pi..."
    ssh $PI_USER@$PI_HOST
}

restart_pi() {
    if ! check_pi; then return; fi
    
    echo "🔄 Restarting Pi..."
    ssh $PI_USER@$PI_HOST "sudo reboot"
    echo "⏳ Pi is restarting... wait 60 seconds"
}

# Main loop
while true; do
    show_menu
    read -p "Choose option: " choice
    
    case $choice in
        1) setup_pi_first_time ;;
        2) copy_script ;;
        3) run_setup ;;
        4) start_voice ;;
        5) stop_voice ;;
        6) check_status ;;
        7) view_logs ;;
        8) ssh_into_pi ;;
        9) restart_pi ;;
        10) clear ; continue ;;
        q|Q) echo "👋 Goodbye!"; exit 0 ;;
        *) echo "❌ Invalid option" ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    clear
done
