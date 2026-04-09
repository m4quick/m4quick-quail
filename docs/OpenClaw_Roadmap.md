# OpenClaw Research & Roadmap

## Active Research Items

### 1. Passkey Roadmap for OpenClaw
**Status**: Research Phase
**Priority**: Medium
**Owner**: TBD

**Description:**
Research and plan WebAuthn/Passkey integration for OpenClaw authentication across all client types.

**Key Questions:**
- [ ] Which WebAuthn library to use? (py-webauthn, fido2, etc.)
- [ ] How to handle cross-device credential sync?
- [ ] Fallback mechanisms for unsupported devices
- [ ] Migration path from current token-based auth
- [ ] Storage of public keys (database format)

**Reference Documents:**
- `/docs/WebUI_Auth_Architecture.md` - Architecture decisions
- WebAuthn spec: https://www.w3.org/TR/webauthn-2/
- Apple Passkey: https://developer.apple.com/documentation/authenticationservices/public-private_key_authentication

**Dependencies:**
- WebUI v2.0+ stable
- Gateway API extensions
- Cross-platform testing

**Estimated Effort**: 2-3 weeks implementation

---

### 2. Authentication Roadmap for OpenClaw
**Status**: Planning Phase
**Priority**: Medium
**Owner**: TBD

**Description:**
Comprehensive authentication strategy for OpenClaw ecosystem including TUI, WebUI, API access, and third-party integrations.

**Current State:**
- TUI: Session-based (implicit trust)
- WebUI: Localhost trust (Phase 1)
- API: Token-based with OpenClaw Gateway

**Target State:**
- Multi-factor options (Passkey, TOTP, hardware keys)
- Granular permissions (read-only, operator, admin)
- Device management (revoke access per device)
- Audit logging (who accessed what, when)

**Research Areas:**
- [ ] Auth provider integration (OAuth2, OIDC)
- [ ] Device fingerprinting for risk-based auth
- [ ] Session management improvements
- [ ] API key vs JWT tradeoffs
- [ ] Rate limiting and brute force protection

**Phased Approach:**

**Phase 1 (Current)**
- Localhost trust model
- Simple token auth for API
- Tailscale for transport security

**Phase 2 (Near-term)**
- Reverse proxy auth layer
- Passkey support for WebUI
- QR code pairing

**Phase 3 (Future)**
- OAuth/OIDC integration
- Enterprise SSO support
- Advanced session management

**Reference Documents:**
- `/docs/WebUI_Auth_Architecture.md`
- Current auth implementation in Gateway

**Dependencies:**
- User demand for remote access
- Enterprise requirements
- Security audit findings

**Estimated Effort**: 4-6 weeks across all phases

---

## Related Work Items

### WebUI Development
- Current: v1.0 (test mode, localhost only)
- Target: v2.0 (production ready, optional auth)
- See: `openclaw-webui/` directory

### Documentation
- `/docs/WebUI_Auth_Architecture.md` - Auth architecture decisions
- `/docs/OpenClaw_Roadmap.md` - This file
- `/memory/2026-04-08.md` - Decision log

## Notes

Research items added: 2026-04-08
Next review: When WebUI v2.0 planning begins

