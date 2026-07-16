# MiniTV Requirements

## REQ-001: HomeAssistant-Triggered Display Alert

**Status:** Done

**Description:**
Implement a flash alert overlay that:
- Listens for `trigger_alert` service calls from Home Assistant via the native ESPHome API.
- Renders a full-screen blinking overlay (1 Hz) with a caller-specified RGB background color.
- Displays custom text provided by the caller (e.g., "Door Opened", "Motion Detected").
- Supports choosing dark or light text via the `alert_font_black` flag for contrast.
- Auto-dismisses after a caller-configurable duration (default 5 000 ms) and returns to the clock.

**Implementation Details:**
- ESPHome `api: services:` exposes `trigger_alert` with parameters:
  - `alert_message` (string)
  - `alert_color_r`, `alert_color_g`, `alert_color_b` (int, 0–255 each)
  - `alert_font_black` (bool)
  - `alert_duration_ms` (int, ≥ 1; defaults to 5 000 when ≤ 0)
- Alert state is stored in `globals:` (`alert_active`, `alert_text`, `alert_start_time`, `alert_color_*`, `alert_font_black`, `alert_duration_ms`).
- The display `lambda` (100 ms interval) auto-dismisses and blends back to clock rendering.

**Traceability:**
- `MiniTV.yaml` — `globals:`, `api:`, `display.lambda`

## REQ-002: Clock Shows Date Alongside Time

**Status:** Done

**Description:**
- Default display mode shows the current time (`HH:MM:SS`).
- The current date (`DD-MM-YYYY`) is shown on a second line below the time.

**Implementation Details:**
- Both lines are rendered via `it.strftime()` in the display `lambda`, using the existing
  `ha_time` (Home Assistant) time source.

**Traceability:**
- `MiniTV.yaml` — `time:`, `display.lambda`

## REQ-003: Waste-Collection Reminder Icons

**Status:** Done

**Description:**
- Read the Home Assistant waste-collection calendar (`calendar.ics`), which contains events
  "Neuenbürg: Glas", "Neuenbürg: Restmüll", "Neuenbürg: Papier", "Neuenbürg: Leichtverpackungen".
- Starting 3 days before a collection, show a small trash-can icon along the bottom of the
  display.
- Icon color indicates the waste type: white = Restmüll, yellow = Leichtverpackung,
  blue = Glas, green = Papier.
- On the last day before collection and on the collection day itself, the icon blinks at
  0.5 Hz (1 s on / 1 s off).
- Each icon shows the number of days remaining until collection (`0` on collection day).
- Multiple icons can be shown simultaneously (e.g., 2 days until Restmüll and 0 days until
  Papier at the same time), laid out horizontally and centred.
- The weekday name is no longer shown, freeing vertical space for the icon row.

**Implementation Details:**
- The device polls the Home Assistant REST Calendar API
  (`GET /api/calendars/calendar.ics?start=...&end=...`) directly over HTTP using the
  `http_request` component, authenticated with a Long-Lived Access Token
  (`!secret ha_token`, formatted as the full `Authorization: Bearer ...` header value).
- Polling runs every 30 minutes (`interval:`), fetching a window from yesterday to +5 days.
- The JSON response is parsed with ArduinoJson (`json:` component); for each event within
  0–3 days of today, the minimum "days until" value is stored per waste type in
  `globals:` (`days_restmuell`, `days_leichtverpackung`, `days_glas`, `days_papier`; `-1`
  means "hidden").
- The display `lambda` draws the `trash_icon` image (tinted per category via
  `BINARY` + `chroma_key` transparency), with the countdown number overlaid, and applies
  the 0.5 Hz blink when `days <= 1`.

**Traceability:**
- `MiniTV.yaml` — `substitutions:`, `globals:`, `json:`, `http_request:`, `interval:`,
  `image:`, `font: (icon_font)`, `display.lambda`
- `src/minitv/Trashcan.png`
