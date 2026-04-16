# Copilot Instructions

## Project Overview
Python-based CLI tool (may include a GUI layer when needed).

Goals:
- Clean architecture
- Strong typing
- Reproducible environment
- First-class documentation
- Easy debugging (VS Code)

This document defines **development rules** and **project hygiene expectations**.

---

## Core Development Principles

### Package & Environment Management
- **Prefer `uv` over `pip`** for dependency and environment management
- Use `pyproject.toml` as the **single source of truth**
- No `requirements*.txt` unless explicitly required by external tooling

```bash
uv venv
uv pip install -e ".[dev]"
```

---

### Python Style & Quality
- **Always use typing / type hints**
  - Public APIs: fully typed
  - Internal code: type where reasonable
- Run `mypy` regularly
- Follow **Google-style docstrings**

Example:
```python
def parse_config(path: Path) -> Config:
    """Parse a configuration file.

    Args:
        path: Path to the configuration file.

    Returns:
        Parsed configuration object.

    Raises:
        ConfigError: If the file is invalid.
    """
```

---

## Repository Documentation (Mandatory)

The following files **must exist and be actively maintained**:

### `README.md`
- Purpose of the tool
- Installation
- Usage examples
- Development setup

### `systemoverview.md`
- High-level architecture
- Responsibilities of modules
- Interactions and data flow
- UML diagrams

### `requirements.md`
- Track **all requirements explicitly given by the user**
- Each requirement must include:
  - ID
  - Description
  - Status (open / in progress / done)
  - Traceability (where implemented)

### `masterplan.md`
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

---

## GUI Development (when applicable)

If the project requires a graphical user interface:

- **Use PySide6** (Qt for Python) — the official Qt binding, preferred over PyQt6 or Tkinter
- Add `pyside6` as a dependency in `pyproject.toml`
- Structure GUI code under `src/<package_name>/gui/`:
  ```text
  gui/
    __init__.py
    app.py          # QApplication setup & entry point
    main_window.py  # Main QMainWindow subclass
    widgets/        # Reusable custom widgets
    dialogs/        # Modal dialogs
    resources/      # Icons, QSS stylesheets, .ui files
  ```
- **Separate business logic from UI**: core logic lives in `core/`, GUI only calls it
- Use Qt Designer (`.ui` files) for complex layouts; load with `QUiLoader` or `uic.loadUi()`
- Apply a consistent stylesheet via a `.qss` file loaded at startup
- **GUI visual style: dark, flat, and sleek** — use a dark color palette, minimal borders, flat buttons, and clean typography. No gradients, no raised frames. Inspired by modern dark-mode design (e.g., VS Code dark theme aesthetics).
- Add a GUI launch configuration to `.vscode/launch.json`
- Prefer signals/slots over direct method calls for UI ↔ logic communication
- Use `QThread` or `QRunnable` for long-running tasks to keep the UI responsive

Example `pyproject.toml` extras:
```toml
[project.optional-dependencies]
gui = ["pyside6"]
```

---

## Tooling & Debugging

### VS Code
- Create and maintain `.vscode/launch.json`
- Debugging must work out-of-the-box for:
  - CLI entry point
  - GUI entry point (if applicable)
  - Modules
  - Tests

---

## Version Control Hygiene

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

## Milestone Completion Protocol

After completing **each milestone**:
1. Run all existing tests: `.venv\Scripts\python.exe -m pytest tests/ -v`
2. Run type check: `.venv\Scripts\python.exe -m mypy src/ --ignore-missing-imports`
3. Commit the current project state with a descriptive message referencing the milestone (e.g., `feat: complete M2 - core infrastructure`)
   - Always include the Co-authored-by trailer
4. If a git remote (origin) is configured, push to the server: `git push`

---

## UI/GUI Design

When doing **any work on UI or GUI**, consult and apply the design principles from **`.github/frontend_design.md`**.

Key principles to apply to PySide6/QSS work:
- Commit to a **bold, intentional aesthetic direction** — not generic
- Use **distinctive typography**: prefer monospace or characterful fonts over defaults
- **Color**: dominant dark background with a sharp, memorable accent color; avoid timid palettes
- **Contrast**: active/selected states must be unambiguously distinct from inactive ones
- **Details matter**: tab bars, scrollbars, checkbox indicators, focus rings — all must be intentional
- **No "AI slop"**: avoid VS Code clone aesthetics — design something genuinely unique to this product

The current design direction for RipTideAl: **"Neon Noir Pirate"** — deep navy/black backgrounds, electric teal (`#00e5b0`) as the primary accent, monospace font influence, high-contrast interactive elements.

---

## Enforcement Rules
- No untyped public APIs
- No undocumented behavior
- Architectural changes require updating:
  - `systemoverview.md`
  - `requirements.md` (if requirement-related)
  - `masterplan.md` (if milestone-related)
- If unsure → **state assumptions explicitly**
