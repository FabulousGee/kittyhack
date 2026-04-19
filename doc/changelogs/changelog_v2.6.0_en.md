# v2.6.0

This release introduces a token-authenticated REST API for remote control and scripted integrations.

> Living document — more entries will be appended as additional pull requests land before the release is cut.

## New Features
- **REST API under `/api/v1/*`**: a small JSON API for controlling the flap from scripts, Home Assistant, Stream Deck, iOS Shortcuts, browser bookmarks and webhooks. Supports:
  - Door control — `door/open`, `door/close`, plus explicit `unlock_inside` / `lock_inside` / `unlock_outside` / `lock_outside` (GET and POST).
  - Mode switching — read (`GET /mode`), set both directions (`PUT /mode`), or change entry and exit direction independently via per-value endpoints (`/mode/entry/{all|all_rfids|known|none|configure_per_cat}`, `/mode/exit/{allow|deny|configure_per_cat}`).
  - Status — combined door state + current mode (`GET /status`).
  - Cats — list all configured cats (`GET /cats`) and toggle `allow_entry` / `allow_exit` / `enable_prey_detection` on a single cat by RFID or name (`PUT /cats/<id>`).
  - Events — recent motion/detection events (`GET /events?limit=N`).
  Door actions are routed through the existing `manual_door_override` mechanism, so all safety rules (max-unlock timeout, prey-detection auto-lock, MQTT mirroring) continue to apply.
- **API token management in the System tab**: create, list and revoke tokens from the Web UI. Tokens are shown only once at creation and stored as SHA-256 hashes in `api_tokens.json` (preserved across updates). Authentication accepts `Authorization: Bearer <token>` header, `X-API-Key: <token>` header, or `?token=<token>` query parameter — the latter specifically so URL-only clients like Stream Deck can trigger actions with a single URL. Failed auth attempts are rate-limited to 10 per source IP per 60 seconds.

## Documentation
- **`CLAUDE.md`** added at the repo root: project orientation notes for AI-assisted development sessions (file map, target-vs-remote architecture, Shiny conventions, config add pattern, i18n workflow, release process, update-flow caveats, WLAN-watchdog design, and a collected list of lessons learned from recent PRs).

## Upgrade notes
- The API is off by default in the sense that no tokens exist yet — no requests can succeed until a token is created. Create tokens under **System → API Tokens** and store the plaintext value shown in the create dialog; it cannot be retrieved again.
- For URL-only clients, use dedicated per-device tokens and revoke them when no longer needed — tokens in URLs may appear in web-server access logs and browser history.
