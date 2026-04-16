# MiniTV

GeekMagic Mini-TV ESPHome configuration repository.

## Purpose

This repository stores the ESPHome configuration and supporting project documentation for a GeekMagic Mini-TV on ESP8266.

## Installation

1. Place `MiniTV.yaml` in your ESPHome config folder.
2. Ensure `secrets.yaml` contains `wifi_ssid` and `wifi_password`.
3. Upload the configuration through ESPHome or Home Assistant.

## Usage

- The display shows a clock when synced to Home Assistant time.
- Use the `trigger_alert` API service to flash a yellow alert with custom text.

## Development

- Edit `MiniTV.yaml` for display and automation changes.
- Maintain documentation in `docs/`.
- Use `pre-commit` to validate YAML and protect secrets.
