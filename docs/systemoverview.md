# System Overview

## Architecture

The MiniTV project is centered on an ESP8266 running ESPHome. The primary responsibilities are:

- `MiniTV.yaml`: ESPHome configuration for Wi-Fi, API, display, and device behavior.
- `docs/`: project documentation and requirements tracking.
- `src/minitv/`: placeholder package structure for repository organization.

## Components

- ESP8266 (`d1_mini`) board
- ST7789v SPI display panel
- PWM backlight control on GPIO5
- Home Assistant time sync via `time:` platform
- API service for external alert triggering

## Data Flow

1. Device boots and enables backlight.
2. ESPHome connects to Wi-Fi and Home Assistant.
3. The display lambda renders either the clock or a yellow alert message.
4. External systems can call `trigger_alert` via Home Assistant API.
