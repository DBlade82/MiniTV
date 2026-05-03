# System Overview

## Architecture

The MiniTV project is an ESP8266-based ESPHome device that displays a clock and can show
push-alert overlays triggered from Home Assistant.

```mermaid
C4Context
    title MiniTV — System Context

    Person(user, "User / Automation", "Home Assistant automation or user")
    System(ha, "Home Assistant", "Orchestration hub — provides time sync and service calls")
    System_Boundary(device, "GeekMagic Mini-TV (ESP8266)") {
        Component(esphome, "ESPHome Runtime", "Wi-Fi, API, OTA, Logger")
        Component(display, "ST7789V Display Lambda", "Renders clock or alert overlay every 100 ms")
        Component(backlight, "PWM Backlight", "GPIO5 — brightness control")
        Component(globals, "Alert State Globals", "alert_active, text, color, timer")
    }

    Rel(user, ha, "Calls trigger_alert service")
    Rel(ha, esphome, "Native API — time + service call")
    Rel(esphome, globals, "Updates alert state on service call")
    Rel(display, globals, "Reads alert state each frame")
    Rel(display, backlight, "Backlight forced on at boot")
```

## Component Responsibilities

| Component | File | Responsibility |
|-----------|------|----------------|
| ESPHome config | `MiniTV.yaml` | Wi-Fi, API, OTA, display, backlight, fonts, alert globals |
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
    Note over DISP: Every 100 ms display lambda runs
    DISP->>DISP: alert_active? No → render clock

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
