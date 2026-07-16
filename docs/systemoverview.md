# System Overview

## Architecture

The MiniTV project is an ESP8266-based ESPHome device that displays a clock and can show
push-alert overlays triggered from Home Assistant, plus waste-collection reminder icons
sourced from a Home Assistant calendar.

```mermaid
C4Context
    title MiniTV — System Context

    Person(user, "User / Automation", "Home Assistant automation or user")
    System(ha, "Home Assistant", "Orchestration hub — time sync, service calls, calendar REST API")
    System_Boundary(device, "GeekMagic Mini-TV (ESP8266)") {
        Component(esphome, "ESPHome Runtime", "Wi-Fi, API, OTA, Logger")
        Component(httpclient, "HTTP Client", "Polls HA Calendar REST API every 30 min")
        Component(display, "ST7789V Display Lambda", "Renders clock, waste icons, or alert overlay every 100 ms")
        Component(backlight, "PWM Backlight", "GPIO5 — brightness control")
        Component(globals, "State Globals", "Alert state + per-waste-type days-until-collection")
    }

    Rel(user, ha, "Calls trigger_alert service")
    Rel(ha, esphome, "Native API — time + service call")
    Rel(httpclient, ha, "GET /api/calendars/calendar.ics (Bearer token)")
    Rel(httpclient, globals, "Updates days_* countdown on each poll")
    Rel(esphome, globals, "Updates alert state on service call")
    Rel(display, globals, "Reads alert + waste-countdown state each frame")
    Rel(display, backlight, "Backlight forced on at boot")
```

## Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| ESPHome config | `src/minitv/MiniTV.yaml` | Wi-Fi, API, OTA, display, backlight, fonts, alert globals, waste-calendar poll |
| Waste icon asset | `src/minitv/Trashcan.png` | Trash-can glyph, tinted per waste type at draw time |
| Docs | `docs/` | Requirements, masterplan, system overview |
| Repo package | `src/minitv/` | Python package stub for repository tooling |

## Hardware Pin Mapping

| Signal | GPIO | d1_mini label |
|--------|------|---------------|
| SPI CLK | GPIO14 | D5 |
| SPI MOSI | GPIO13 | D7 |
| Display D/C | GPIO0 | D3 |
| Display RESET | GPIO2 | D4 |
| Backlight PWM | GPIO5 | D1 |

## Data Flow

```mermaid
sequenceDiagram
    participant HA as Home Assistant
    participant ESP as ESP8266 (ESPHome)
    participant DISP as ST7789V Display

    HA-->>ESP: Time sync (homeassistant platform)
    Note over ESP: Every 30 min (http_request + interval)
    ESP->>HA: GET /api/calendars/calendar.ics?start=...&end=...
    HA-->>ESP: Events JSON (Glas/Restmüll/Papier/Leichtverpackungen)
    ESP->>ESP: Parse JSON → update days_* globals

    Note over DISP: Every 100 ms display lambda runs
    DISP->>DISP: alert_active? No → render clock + date + waste icons

    HA->>ESP: trigger_alert(message, color, duration_ms)
    ESP->>ESP: Set alert globals (active=true, text, color, start_time)
    DISP->>DISP: alert_active? Yes → render blinking overlay
    Note over DISP: After duration_ms elapses
    DISP->>DISP: alert_active=false → return to clock
```

## Alert State Machine

```mermaid
stateDiagram-v2
    [*] --> Clock : Boot / time synced
    Clock --> Syncing : Time not valid
    Syncing --> Clock : now.is_valid()
    Clock --> AlertBlink : trigger_alert received
    AlertBlink --> AlertBlink : elapsed < duration_ms\n(1 Hz blink: color / black phases)
    AlertBlink --> Clock : elapsed >= duration_ms
```

## Waste-Collection Icon Logic

```mermaid
stateDiagram-v2
    [*] --> Hidden : days == -1 (no collection within 3 days)
    Hidden --> Steady : 2 <= days <= 3
    Steady --> Blinking : days <= 1 (last day before / collection day)
    Blinking --> Hidden : next poll clears the category
```
