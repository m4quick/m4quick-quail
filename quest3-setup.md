# OpenClaw WebUI on Meta Quest 3

## Quick Start (No Sideloading Required)

### 1. Network Setup
Your Quest 3 needs to be on the **same WiFi** as your Mac Studio.

**Check your Mac's local IP:**
```
192.168.1.168  ← WebUI is running here on port 5001
```

### 2. Open Meta Quest Browser
1. Put on Quest 3
2. Press **Oculus button** → Open **Meta Quest Browser** (looks like a compass icon)
3. Type URL: `http://192.168.1.168:5001`
4. Should load your WebUI immediately

### 3. Enable WebXR (if prompted)
When the AR dashboard loads:
- Browser may ask for **XR permissions** — click "Allow"
- For hand tracking: Go to Settings → Experimental → Enable "Hand Tracking"

### 4. Controls
- **Controllers:** Point and click like laser pointer
- **Hand Tracking:** Pinch to select, grab to move
- **Voice:** Double-tap Oculus button → "Hey Facebook" (or use WebUI mic button)

---

## Developer Mode (For Testing)

If you want to install native apps later:

1. **Install Meta Quest Developer Hub** on Mac:
   ```bash
   brew install --cask meta-quest-developer-hub
   ```

2. **Enable Developer Mode on Quest:**
   - Meta Quest app (iPhone/Android) → Devices → Quest 3 → Developer Mode → ON
   - Or: Headset Settings → System → Developer → Enable

3. **Connect via USB-C** for debugging

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Can't reach site" | Check Mac firewall: `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off` (temporarily) |
| WebXR not working | Enable in Quest Settings → Experimental Features |
| No hand tracking | Settings → Movement Tracking → Hand Tracking → ON |
| Laggy | Close other Quest apps; check WiFi signal |

---

## Next: AR Features

Once basic WebUI loads, we'll add:
- **WebXR layer** ( immersive mode)
- **Hand tracking gestures**
- **Spatial dashboard panels**
- **Voice commands**

Test URL: `http://192.168.1.168:5001` (working now)

Future AR URL: `http://192.168.1.168:5001/ar`
