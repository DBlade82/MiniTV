# Copilot Instructions

## Project Context
- This workspace targets a GeekMagic Mini-TV flashed with ESPHome on ESP8266 (`d1_mini` / ESP-12F class hardware).
- Primary config file is `src/minitv/MiniTV.yaml`.

## ESPHome Rules For This Project
- Treat missing `secrets.yaml` errors as a first-class setup issue. Either:
  - create `/config/esphome/secrets.yaml`, or
  - replace `!secret` references with direct string values.
- Keep Wi-Fi security explicit: under `wifi:`, set `min_auth_mode: WPA2` unless router limitations require WPA.
- Avoid duplicate GPIO usage. A pin cannot be claimed by multiple components at once.

## GeekMagic Mini-TV Display Notes
- Typical wiring used in this project:
  - SPI clock: GPIO14
  - SPI MOSI: GPIO13
  - D/C: GPIO0
  - Reset: GPIO2
  - Backlight: GPIO5
- The panel is commonly 240x240, but ESP8266 RAM constraints can require reduced render size as a fallback.
- If display is black after successful flash, prioritize this order:
  1. Verify backlight polarity (`backlight_pin.inverted: true/false`).
  2. Render obvious debug graphics (solid background + border) before drawing text.
  3. Ensure text coordinates are computed from `it.get_width()` / `it.get_height()`.
  4. Try reduced dimensions (e.g. 120x120) only as a memory fallback.

## Verified HW Setup (Current)
- Keep this known-good baseline unless debugging requires a targeted change:
  - Display driver: `display.platform: mipi_spi`, `model: st7789v`
  - SPI bus: `spi.id: spihwd`, `interface: hardware`, `clk_pin: GPIO14`, `mosi_pin: GPIO13`
  - Display pins: `dc_pin: GPIO00`, `reset_pin: GPIO02`
  - Display config: `dimensions: 240x240`, `color_depth: 8`, `spi_mode: mode3`, `invert_colors: true`
  - Transform fields must all be explicit when used: `swap_xy`, `mirror_x`, `mirror_y`
  - Backlight control: `esp8266_pwm` on `GPIO5`, with `light` id `backlight`
  - Backlight safety: force `light.turn_on` to `brightness: 100%` in `esphome.on_boot`

## External Component Compatibility
- Some community ST7789 no-frame-buffer forks can break on newer ESPHome versions.
- If a build error mentions component registration conflicts (registered twice / not inheriting from Component), remove incompatible `external_components` override and use built-in drivers first.

## Demo Display Behavior
- Keep a simple clock demo available:
  - `time:` via `platform: homeassistant`
  - `display.lambda` renders "Syncing" until `now.is_valid()`.
  - Then render `%H:%M:%S` centered.

## YAML Configuration Best Practices
- ESPHome YAML is the primary language for this project; write clean, properly indented YAML
- Group related components (e.g., all GPIO pins, all light definitions)
- Use meaningful identifiers and comments to document non-obvious configuration
- Validate syntax before suggesting changes; ESPHome CLI will catch typos
- When writing any code (lambdas, custom logic), follow style guidelines in `.github/python_code.md` if available

## Troubleshooting Workflow
- First fix validation/build errors.
- Then fix hardware-visible issues (backlight, pin mapping, geometry).
- Keep changes minimal and test one variable at a time.

## Repository Documentation (Mandatory)

The following files **must exist and be actively maintained**:

### `docs/requirements.md`
- Track **all requirements explicitly given by the user**
- Each requirement must include:
  - ID
  - Description
  - Status (open / in progress / done)
  - Traceability (where implemented)

### `README.md`
- Purpose of the tool
- Installation
- Usage examples
- Development setup

### `docs/systemoverview.md`
- High-level architecture
- Responsibilities of modules
- Interactions and data flow
- UML diagrams

### `docs/masterplan.md`
- Milestones
- Current focus
- Progress tracking
- Risks and technical debt

---

## Markdown Diagrams
- For all `.md` files, **prefer Mermaid and PlantUML** for diagrams
- **Do not use ASCII art** for architecture, flows, or diagrams
- Diagrams must be:
  - Renderable in common Markdown viewers
  - Source-controlled and readable as text

Preferred:
- Mermaid (flows, sequences, state diagrams)
- PlantUML (components, C4, complex interactions)

## Version Control Hygiene

if workspace folder is not a git repo yet, initialize it with `git init` and make an initial commit with all project relevant existing files. Then create a new branch named `main` and set it as the default branch.

### `.gitignore`
- Create and maintain a `.gitignore` file
- Must cover:
  - Virtual environments (`.venv/`)
  - Build artifacts
  - Test caches
  - OS / IDE junk files
- Keep it minimal and intentional

### `.gitattributes` & Git LFS
- Create and maintain a `.gitattributes` file
- Any binaries that must be committed **must be tracked via Git LFS**

Rules:
- Identify binary formats early (`.bin`, `.zip`, `.exe`, `.elf`, large `.pdf`, etc.)
- Ensure LFS tracking is explicit and documented
- No large binaries committed directly to Git history

Example:
```gitattributes
*.bin filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
```

---

## Project Structure (Target)

```text
src/
  <package_name>/
    __init__.py
    __main__.py
    cli.py
    commands/
    core/
    gui/              # optional — only when a GUI is needed
      __init__.py
      app.py
      main_window.py
      widgets/
      dialogs/
      resources/
tests/
docs/
  systemoverview.md
  requirements.md
  masterplan.md
pyproject.toml
.vscode/
  launch.json
```

---

## Secrets & Pre-commit Hooks

Every repository **must** be protected against accidental secret commits:

1. Add `pre-commit` to `[project.optional-dependencies] dev`
2. Create `.pre-commit-config.yaml` at the repo root with **Gitleaks** as the primary secrets scanner
3. After cloning or initial setup, always run: `pre-commit install`
4. Gitleaks will run automatically on every `git commit` and block the commit if secrets are detected
5. Also include standard hygiene hooks: trailing whitespace, end-of-file fixer, check-yaml, check-json

Example `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
```

---

## Milestone Completion Protocol

After completing **each milestone**:
1. Run all existing tests: `.venv\Scripts\python.exe -m pytest tests/ -v`
2. Run type check: `.venv\Scripts\python.exe -m mypy src/ --ignore-missing-imports`
3. Commit the current project state with a descriptive message referencing the milestone (e.g., `feat: complete M2 - core infrastructure`)
   - Always include the Co-authored-by trailer
4. If a git remote (origin) is configured, push to the server: `git push`

---
