# v2.6.0

Dieses Release führt eine token-authentifizierte REST-API für Remote-Steuerung und Skript-Integrationen ein.

> Lebendes Dokument — weitere Einträge werden ergänzt, sobald zusätzliche Pull-Requests vor dem Release landen.

## Neue Features
- **REST-API unter `/api/v1/*`**: eine kompakte JSON-API, um die Klappe aus Skripten, Home Assistant, Stream Deck, iOS Shortcuts, Browser-Lesezeichen und Webhooks zu steuern. Enthalten sind:
  - Klappensteuerung — `door/open`, `door/close`, sowie explizit `unlock_inside` / `lock_inside` / `unlock_outside` / `lock_outside` (GET und POST).
  - Modus-Wechsel — aktuellen Modus auslesen (`GET /mode`), beide Richtungen setzen (`PUT /mode`) oder Eingangs- und Ausgangsrichtung einzeln per Wert-Endpunkt wechseln (`/mode/entry/{all|all_rfids|known|none|configure_per_cat}`, `/mode/exit/{allow|deny|configure_per_cat}`).
  - Status — kombinierter Klappen- und Modus-Zustand (`GET /status`).
  - Katzen — alle konfigurierten Katzen auflisten (`GET /cats`) und `allow_entry` / `allow_exit` / `enable_prey_detection` pro Katze per RFID oder Name umschalten (`PUT /cats/<id>`).
  - Events — die letzten Bewegungs- und Erkennungs-Events (`GET /events?limit=N`).
  Klappenbefehle laufen über den bestehenden `manual_door_override`-Pfad — alle Sicherheitsregeln (maximale Entriegelungsdauer, automatische Verriegelung bei Beute-Erkennung, MQTT-Spiegelung) greifen weiterhin.
- **API-Token-Verwaltung im System-Tab**: Tokens direkt in der WebGUI erstellen, auflisten und widerrufen. Der Token wird nur einmal bei der Erstellung angezeigt und als SHA-256-Hash in `api_tokens.json` gespeichert (überlebt Updates). Die Authentifizierung akzeptiert den `Authorization: Bearer <token>`-Header, den `X-API-Key: <token>`-Header oder den `?token=<token>`-Query-Parameter — letzteres speziell für URL-only-Clients wie Stream Deck, die Aktionen mit einer einzigen URL auslösen. Fehlgeschlagene Versuche werden pro Quell-IP auf 10 innerhalb von 60 Sekunden begrenzt.

## Verbesserungen
- **Benutzerdefiniertes Update-Repository akzeptiert jetzt auch GitHubs PR-Kurzform**: Das Feld *Konfiguration → Update-Repository* erkennt zusätzlich zu `owner/repo` und `owner/repo@branch-oder-tag` auch `owner:branch` (z. B. `FabulousGee:feat/rest-api`). Werte können damit direkt aus dem Kopf einer Pull-Request-Seite auf github.com kopiert werden. Beim Speichern wird der Wert intern in die kanonische `owner/repo@branch`-Form normalisiert, damit die Konfigurationsdatei unabhängig von der Eingabeform sauber bleibt.

## Dokumentation
- **`CLAUDE.md`** im Projekt-Root: Orientierungs-Notizen für KI-gestützte Entwicklungs-Sitzungen (Datei-Übersicht, Target-vs-Remote-Architektur, Shiny-Konventionen, Pattern für neue Config-Felder, i18n-Workflow, Release-Prozess, Stolperfallen beim Update-Flow, WLAN-Watchdog-Design sowie eine gesammelte Liste der Erkenntnisse aus den letzten PRs).

## Hinweise zum Upgrade
- Die API ist im Auslieferungszustand „leer" — es existieren keine Tokens, kein Aufruf gelingt, bis ein Token erstellt wird. Unter **System → API-Tokens** einen Token anlegen und den bei der Erstellung angezeigten Klartext sicher speichern; er lässt sich später nicht erneut anzeigen.
- Für URL-only-Clients am besten einen eigenen Token pro Gerät anlegen und bei Bedarf widerrufen — Tokens in URLs können in Webserver-Logs und im Browser-Verlauf landen.
