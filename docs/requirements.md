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
