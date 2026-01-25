# Plugin Status Checker Skill

Automated verification system for the ZTL Digital Intelligence Operations Center's multi-agent plugin ecosystem.

## Overview

This skill provides comprehensive health checks for the project's 8 business group plugins and 60+ specialized agents. It verifies configuration files, directory structures, and generates detailed status reports.

## Structure

```
plugin-status/
├── SKILL.md                          # Skill metadata and usage guide
├── scripts/
│   └── verify_plugins_core.py        # Python execution engine
└── README.md                         # This file
```

## Features

### Configuration Validation
- ✅ Checks `.claude/settings.json` for enabled plugins
- ✅ Validates `.claude-plugin/marketplace.json` definitions
- ✅ Verifies all 8 business group plugins are properly configured

### Structure Integrity
- ✅ Confirms plugin directories exist in `plugins/`
- ✅ Validates `agents/` subdirectories
- ✅ Counts and lists all agent definition files

### Comprehensive Reporting
- ✅ Total agent count (expected: 62 agents)
- ✅ Per-group statistics:
  - 战略组 (Strategy): 9 agents
  - 创意组 (Creative): 6 agents
  - 情报组 (Intelligence): 8 agents
  - 筹建组 (Construction): 6 agents
  - 开发组 (Development): 11 agents
  - 美团组 (Meituan Ops): 6 agents
  - 供应组 (Supply Chain): 7 agents
  - 行政组 (Admin): 9 agents
- ✅ Overall system health assessment

## Usage

### Via Claude Code (Recommended)

Simply ask Claude to check the plugin status:

```
"Check if all plugins are properly activated"
"Verify the plugin system integrity"
"Show me the current plugin status"
```

Claude will automatically discover and invoke this skill.

### Direct Python Execution

**Human-readable output**:
```bash
python3 .claude/skills/项目插件配置状态检查/plugin-status/scripts/verify_plugins_core.py
```

**JSON output** (for programmatic use):
```bash
python3 .claude/skills/项目插件配置状态检查/plugin-status/scripts/verify_plugins_core.py --json
```

**Specify project root**:
```bash
python3 .claude/skills/项目插件配置状态检查/plugin-status/scripts/verify_plugins_core.py --project-root /path/to/project
```

## Output Examples

### Successful Check
```
✓ All plugins operational
✓ 8/8 plugins enabled
✓ 62 agents detected
✓ System ready for multi-agent orchestration
```

### Issues Detected
```
⚠ Configuration issues found:
  - Plugin X not enabled in settings.json
  - Plugin Y directory missing
  - Expected 9 agents in Strategy group, found 8
```

## Integration

### CI/CD Pipeline
```yaml
# .github/workflows/verify-plugins.yml
- name: Verify Plugin System
  run: |
    python3 .claude/skills/项目插件配置状态检查/plugin-status/scripts/verify_plugins_core.py
    if [ $? -ne 0 ]; then
      echo "Plugin system verification failed"
      exit 1
    fi
```

### Startup Script
```bash
#!/bin/bash
# startup.sh
echo "Verifying plugin system..."
python3 .claude/skills/项目插件配置状态检查/plugin-status/scripts/verify_plugins_core.py
if [ $? -eq 0 ]; then
  echo "System ready, starting application..."
  npm start
else
  echo "Plugin system issues detected, aborting startup"
  exit 1
fi
```

### Python Integration
```python
from pathlib import Path
from scripts.verify_plugins_core import PluginStatusChecker

# Create checker
checker = PluginStatusChecker(project_root=Path.cwd())

# Run verification
exit_code = checker.run(json_output=False)

if exit_code == 0:
    print("All systems operational")
else:
    print("Issues detected, check logs")
```

## Technical Details

### Files Monitored
- `.claude/settings.json` → Plugin activation configuration
- `.claude-plugin/marketplace.json` → Plugin registry
- `plugins/[业务组]/` → Plugin directories
- `plugins/[业务组]/agents/*.md` → Agent definitions

### Exit Codes
- `0` - All checks passed, system healthy
- `1` - Issues detected, review required

### Color Codes (Terminal Output)
- 🟢 Green `✓` - Check passed
- 🔴 Red `✗` - Check failed
- 🟡 Yellow `⚠` - Warning/issues detected
- 🔵 Blue - Section headers

## When to Use

**Recommended Usage Scenarios**:
- 🔧 After plugin configuration changes
- 🚀 Before major operations or deployments
- 🐛 Troubleshooting missing agents
- 💻 System startup health checks
- 📊 Generating system inventory reports

## Maintenance

### Updating Expected Plugin List

If you add/remove business groups, update the `expected_plugins` list in `verify_plugins_core.py`:

```python
expected_plugins = [
    "strategy-team@ztl-local-plugins",
    "creative-team@ztl-local-plugins",
    # ... add new plugins here
]
```

### Updating Business Group Mapping

Update the `business_groups` dictionary for new groups:

```python
business_groups = {
    "战略组": "strategy-team",
    "创意组": "creative-team",
    # ... add new groups here
}
```

## Related Scripts

This skill is based on and replaces:
- `scripts/verify-plugins.py` - Original standalone verification script

The core logic has been modularized into a reusable skill package for better integration with Claude Code's capability discovery system.

## License

Part of the ZTL Digital Intelligence Operations Center project.
