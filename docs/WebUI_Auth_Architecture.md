# OpenClaw WebUI Authentication Architecture

## Overview
A dedicated web interface for OpenClaw, designed for cross-platform compatibility including potential Meta AR applications.

## Authentication Strategy: Hybrid (Passkey + QR Fallback)

### Current Approach (Phase 1)
- **Localhost Trust**: WebUI runs on same machine as OpenClaw Gateway
- **No auth required** for localhost connections (127.0.0.1, 192.168.1.x)
- **Tailscale** provides encrypted transport for remote access
- **Test mode**: Simple echo responses for UI validation

### Future Enhancement (Phase 2)
**Reverse Proxy Layer** for authentication:
```
Client → Auth Proxy (Passkey/QR) → OpenClaw Gateway
```

**Why This Approach:**
- ✅ Keeps OpenClaw core simple
- ✅ Adds auth as independent layer
- ✅ Easy to retrofit later
- ✅ No database migrations needed

## Client Support

### 1. Mobile (Android/iOS)
- **Primary**: Passkey (FaceID/TouchID)
- **Fallback**: QR code pairing
- Storage: Platform keychain (iCloud Keychain, Google)

### 2. Mac Client
- **Same machine**: No auth (localhost)
- **Remote**: Passkey + TouchID
- Storage: macOS Keychain

### 3. Windows Client
- **Remote only**: Passkey + Windows Hello
- Storage: Windows Credential Manager

## Implementation Notes

### Retrofit Strategy
If adding auth later:
1. Add nginx/auth proxy in front of OpenClaw
2. Keep existing localhost access (backward compatible)
3. New remote connections require Passkey/QR
4. No changes to OpenClaw core

### Why Not Implement Now?
- Current use case: Single user, local access
- Tailscale provides transport security
- Auth adds complexity without immediate benefit
- Easy to add later via proxy layer

## Security Considerations

### Current (No Auth)
- **Risk**: Anyone on local network can access if they know IP:port
- **Mitigation**: Firewall, Tailscale, obscurity
- **Acceptable for**: Single user, home network

### Future (With Auth)
- **Protection**: Passkey prevents credential theft
- **QR Fallback**: Allows legacy device support
- **Origin-bound**: Phishing-resistant

## Decision Log

**2026-04-08**: Decided to defer Passkey implementation
- Use localhost trust model for now
- Document architecture for future retrofit
- Plan reverse proxy approach for auth layer

## Open Questions

1. Should auth be core OpenClaw feature or external proxy?
   - Decision: External proxy (nginx/auth service)

2. Priority level?
   - Decision: Nice-to-have, not essential for v1

3. Start with WebUI only?
   - Decision: Yes, TUI uses existing session auth

## References

- WebAuthn spec: https://www.w3.org/TR/webauthn-2/
- Passkey docs: https://developer.apple.com/documentation/authenticationservices/public-private_key_authentication/supporting_passkeys
- Tailscale: https://tailscale.com/
