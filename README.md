# MiniTV

ESPHome configuration for a **GeekMagic Mini-TV** running on an ESP8266, showing a live
clock and customizable push-alert overlays triggered from Home Assistant.

## Features

- Full-screen **clock** synchronized from Home Assistant.
- **Alert overlay** triggered via a Home Assistant service call — configurable text, color, duration, and blink rate.
- 8-bit color, 240×240 ST7789V SPI panel with hardware SPI at 40 MHz.
- OTA firmware updates via ESPHome dashboard.
- PWM backlight control exposed as a Home Assistant light entity.

## Hardware

| Item | Detail |
|------|--------|
| Board | GeekMagic Mini-TV (ESP8266 / ESP-12F / d1_mini pinout) |
| Display | ST7789V 240×240 SPI |
| SPI CLK | GPIO14 (D5) |
| SPI MOSI | GPIO13 (D7) |
| D/C | GPIO0 (D3) |
| Reset | GPIO2 (D4) |
| Backlight | GPIO5 (D1), PWM |

## Installation

1. Copy `MiniTV.yaml` into your ESPHome config folder (e.g. `/config/esphome/`).
2. Create `/config/esphome/secrets.yaml` (never commit this file):
   ```yaml
   wifi_ssid: "YourSSID"
   wifi_password: "YourPassword"
   wifi_recover_password: "RecoveryAPPassword"
   ```
3. Flash:
   ```bash
   esphome run MiniTV.yaml
   ```

## Usage

### Clock mode

The display shows `HH:MM:SS` centered on a black background once time is synced from Home
Assistant. During the brief boot window it shows `Syncing`.

### Trigger an alert from Home Assistant

Call the service `esphome.minitv_trigger_alert` from an automation, script, or Developer Tools:

```yaml
service: esphome.minitv_trigger_alert
data:
  alert_message: "Motion detected!"
  alert_color_r: 255
  alert_color_g: 200
  alert_color_b: 0
  alert_font_black: false   # true for dark text on bright backgrounds
  alert_duration_ms: 5000   # ms; use 0 for the default 5 000 ms
```

The display blinks at 1 Hz (color phase / black phase) for the specified duration, then
returns to the clock.

## Development

### Prerequisites

- [ESPHome](https://esphome.io) 2024.x or later
- Python ≥ 3.10 (for pre-commit hooks)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

```bash
# Install pre-commit hooks (one-time, prevents accidental secret commits)
pip install pre-commit
pre-commit install
```

### Linting / validation

```bash
pre-commit run --all-files       # YAML lint + secrets scan
esphome config MiniTV.yaml       # ESPHome syntax check (requires ESPHome CLI)
```

### Repository layout

```
MiniTV.yaml          # ESPHome configuration (primary deliverable)
docs/
  requirements.md    # Tracked requirements with status
  systemoverview.md  # Architecture diagrams
  masterplan.md      # Milestones and risks
src/minitv/          # Python package stub
tests/               # Placeholder tests
.pre-commit-config.yaml
```

## Security

- Wi-Fi credentials and the recovery AP password are kept in `secrets.yaml`, which is
  excluded from version control by `.gitignore`.
- Gitleaks runs on every commit via pre-commit to block accidental secret exposure.
- The web server is enabled for local debugging; disable it in production by removing
  the `web_server:` block from `MiniTV.yaml`.

