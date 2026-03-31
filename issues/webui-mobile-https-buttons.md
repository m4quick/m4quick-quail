# WebUI Mobile HTTPS Button Issue

**Status:** Open  
**Reported:** 2026-05-14  
**Reporter:** Sir (iPhone 17 Pro)  
**Environment:** Safari + Chrome on iPhone 17 Pro, HTTPS via Tailscale

---

## Problem

Buttons in the OpenClaw WebUI do not respond when accessed via HTTPS on mobile browsers (tested: Safari and Chrome on iPhone 17 Pro).

- HTTP: Buttons work normally
- HTTPS: Buttons are unresponsive (no visual feedback, no action triggered)

---

## Environment Details

| Setting | Value |
|---------|-------|
| Device | iPhone 17 Pro |
| Browsers Tested | Safari (latest), Chrome (latest) |
| Connection | Tailscale HTTPS |
| Working | HTTP (port 80 or custom) |
| Broken | HTTPS (any SSL/TLS endpoint) |

---

## Suspected Cause

WebSocket connection likely failing to upgrade from HTTP to WSS (secure WebSocket) when served over HTTPS. Browser security policies prevent mixed content or insecure WebSocket connections on secure pages.

Possible specific causes:
1. **WebSocket URL hardcoded to `ws://`** instead of dynamic `wss://` when page is HTTPS
2. **Self-signed certificate not trusted** by iOS (even on Tailscale)
3. **CSP (Content Security Policy)** blocking WebSocket connections
4. **Tailscale HTTPS certificate chain** issues on mobile

---

## Diagnostic Steps to Try

### 1. Check WebSocket Connection Status
- Look for connection indicator in WebUI (dot color, "connected" text)
- If showing "disconnected" or flashing red, WebSocket is failing

### 2. Browser Console Debugging
**Requires Mac + USB cable:**
1. Connect iPhone to Mac
2. Safari → Develop → [iPhone Name] → [WebUI tab]
3. Look for:
   - WebSocket connection errors
   - CSP violations
   - Mixed content warnings
   - Certificate errors

### 3. Test WebSocket Directly
Try connecting to WebSocket endpoint manually:
```javascript
// In browser console
const ws = new WebSocket('wss://<your-tailscale-url>/ws');
ws.onopen = () => console.log('Connected');
ws.onerror = (e) => console.error('WS Error:', e);
```

### 4. Check Tailserve Configuration
- Verify WebSocket upgrade headers are properly forwarded
- Check if WebSocket path is correctly routed
- Confirm `wss://` URLs are generated when page is HTTPS

---

## Related Context

- "Mac thinks the buttons don't work because Java [Script] behaves different using HTTP"
- Same behavior across Safari and Chrome suggests server/config issue, not browser-specific

---

## Next Actions

- [ ] Get browser console logs from iPhone via Safari Web Inspector
- [ ] Verify WebSocket URL generation in WebUI code (should use `wss://` for HTTPS pages)
- [ ] Check if Tailscale HTTPS certs are properly trusted by iOS
- [ ] Test with Tailscale Funnel vs direct Tailscale IP
- [ ] Consider adding WebSocket connection status indicator if not present

---

## Notes

- HTTP works → WebUI code is functional
- HTTPS fails → Likely WebSocket upgrade or cert issue
- Both browsers affected → Not a Safari-specific quirk

