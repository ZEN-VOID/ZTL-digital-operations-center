# Skills

This directory contains skills for this plugin.

## Structure

Skills should follow the standard directory structure:

```
skill-name/
├── SKILL.md              # Required: Metadata + Usage
├── scripts/              # Optional: Execution scripts
├── templates/            # Optional: Templates
└── reference.md          # Optional: Extended documentation
```

## Available Skills

### webapp-testing

**Description**: Toolkit for interacting with and testing local web applications using Playwright.

**Capabilities**:
- Verify frontend functionality
- Debug UI behavior
- Capture browser screenshots
- View browser console logs
- Manage server lifecycle (supports multiple servers)

**Key Files**:
- `SKILL.md` - Usage guide and best practices
- `scripts/with_server.py` - Server lifecycle management helper
- `examples/` - Common automation patterns:
  - `element_discovery.py` - Discovering UI elements
  - `static_html_automation.py` - Testing static HTML files
  - `console_logging.py` - Capturing console logs

**Usage Pattern**:
1. Run helper scripts with `--help` first to see usage
2. Use `with_server.py` to manage server lifecycle
3. Write Playwright scripts for automation
4. Follow reconnaissance-then-action pattern for dynamic apps

## Examples

See `.claude/skills/元skills/skills/` for skill creation guidance.
