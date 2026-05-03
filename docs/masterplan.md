# Master Plan

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Project setup and repository scaffolding | ✅ Done |
| 2 | Stable ESPHome configuration for GeekMagic Mini-TV | ✅ Done |
| 3 | Alert service integration with Home Assistant | ✅ Done |
| 4 | Display reliability and hardware troubleshooting | ✅ Done |
| 5 | Documentation refresh, secrets audit, remote publish | 🔄 In Progress |

## Current Focus

- All core milestones completed.
- Keeping documentation current with implemented behavior.
- Maintaining pre-commit hooks and gitleaks scanning to guard against accidental secret commits.

## Progress Notes

- M1–M4 completed across initial commits.
- Display driver fixed after ESPHome Builder update (switched to `mipi_spi` / `st7789v`).
- Alert system fully implemented with configurable duration, color, and blink behavior.

## Risks and Technical Debt

| Risk | Severity | Mitigation |
|------|----------|------------|
| ESP8266 RAM limits with 240×240 display | Medium | Use `color_depth: 8`; fall back to 120×120 if needed |
| ESPHome version regressions | Medium | Pin component versions; test before upgrading |
| Recovery AP password in secrets | Low | `wifi_recover_password` correctly uses `!secret` |
| Google Fonts availability at compile time | Low | Mirror fonts locally if offline builds are needed |
