# Master Plan

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Project setup and repository scaffolding | ✅ Done |
| 2 | Stable ESPHome configuration for GeekMagic Mini-TV | ✅ Done |
| 3 | Alert service integration with Home Assistant | ✅ Done |
| 4 | Display reliability and hardware troubleshooting | ✅ Done |
| 5 | Documentation refresh, secrets audit, remote publish | ✅ Done |
| 6 | Clock date display and waste-collection reminder icons | ✅ Done |
| 7 | Modular multi-device ESPHome package structure | ✅ Done |

## Current Focus

- All core milestones completed.
- Keeping documentation current with implemented behavior.
- Maintaining pre-commit hooks and gitleaks scanning to guard against accidental secret commits.
- Verifying waste-collection icon behaviour against the live Home Assistant calendar once
  flashed to hardware (JSON parsing/date math validated at compile time only so far).

## Progress Notes

- M1–M4 completed across initial commits.
- Display driver fixed after ESPHome Builder update (switched to `mipi_spi` / `st7789v`).
- Alert system fully implemented with configurable duration, color, and blink behavior.
- Clock now shows date (`DD-MM-YYYY`) below the time.
- Waste-collection icons added: device polls Home Assistant's Calendar REST API directly
  (`calendar.ics`) using a Long-Lived Access Token, computes days-until-collection per
  waste type, and renders tinted/blinking icons with a countdown number along the bottom
  of the display; the weekday line was removed to make room. Digit colour is now computed
  at draw time (relative-luminance contrast) for maximum legibility on any icon tint.
- Refactored into a modular ESPHome `packages:` structure (`src/common/minitv-common.yaml`)
  so additional physical MiniTV units can be added via a slim per-device YAML
  (see `src/templates/new-device.yaml.example`) without duplicating shared logic.

## Risks and Technical Debt

| Risk | Severity | Mitigation |
|------|----------|------------|
| ESP8266 RAM limits with 240×240 display | Medium | Use `color_depth: 8`; fall back to 120×120 if needed |
| ESPHome version regressions | Medium | Pin component versions; test before upgrading |
| Recovery AP password in secrets | Low | `wifi_recover_password` correctly uses `!secret` |
| Google Fonts availability at compile time | Low | Mirror fonts locally if offline builds are needed |
| Waste-calendar summary text match (`Restmüll`, `Glas`, etc.) | Low | Substring match is tolerant of prefixes like "Neuenbürg: "; revisit if HA calendar naming changes |
| Home Assistant unreachable during poll | Low | `on_error` logs and retries on the next 30-min interval; countdown globals simply keep their last known value |
