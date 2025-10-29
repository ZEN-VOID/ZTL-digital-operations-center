---
name: plugin-status
description: Comprehensive plugin system status verification for ZTL project. Checks settings.json configuration, marketplace.json definitions, plugin directory structures, and agent statistics across all 8 business groups.
---

# Plugin Status Checker

Automated verification system for the ZTL Digital Intelligence Operations Center plugin ecosystem.

## Quick Start

**Check full plugin system status**:
```
"Check if all plugins are properly activated"
"Verify the plugin system integrity"
"Show me the current plugin status"
```

**The skill will automatically**:
1. ✅ Verify `.claude/settings.json` - enabled plugins configuration
2. ✅ Check `.claude-plugin/marketplace.json` - plugin definitions
3. ✅ Validate plugin directory structures in `plugins/`
4. ✅ Count agents across all 8 business groups
5. ✅ Generate comprehensive status report

## What This Skill Does

This skill performs a comprehensive health check of the ZTL project's multi-agent plugin system:

### Configuration Validation
- Verifies that all 8 business group plugins are enabled in settings.json
- Checks marketplace.json for proper plugin definitions
- Validates plugin source paths exist

### Structure Integrity
- Confirms each plugin directory exists
- Verifies agents/ subdirectory presence
- Counts and lists all agent definition files (.md)

### Statistics Reporting
- Total agent count across the system (expected: 60+)
- Per-group agent breakdown:
  - 战略组 (Strategy): 9 agents
  - 创意组 (Creative): 6 agents
  - 情报组 (Intelligence): 8 agents
  - 筹建组 (Construction): 6 agents
  - 开发组 (Development): 11 agents
  - 美团组 (Meituan Ops): 6 agents
  - 供应组 (Supply Chain): 7 agents
  - 行政组 (Admin): 9 agents

### System Readiness
- Overall health assessment
- Identification of missing or misconfigured plugins
- Ready/Not Ready final status

## Expected Output

**Successful Check**:
```
✓ All plugins operational
✓ 8/8 plugins enabled
✓ 62 agents detected
✓ System ready for multi-agent orchestration
```

**Issues Detected**:
```
⚠ Configuration issues found:
  - Plugin X not enabled in settings.json
  - Plugin Y directory missing
  - Expected 9 agents in Strategy group, found 8
```

## Technical Details

### Files Checked
- `.claude/settings.json` → `enabledPlugins` configuration
- `.claude-plugin/marketplace.json` → `plugins[]` array
- `plugins/[业务组]/` → directory existence
- `plugins/[业务组]/agents/*.md` → agent definitions

### Expected Plugins
1. `strategy-team@ztl-local-plugins`
2. `creative-team@ztl-local-plugins`
3. `intelligence-team@ztl-local-plugins`
4. `construction-team@ztl-local-plugins`
5. `development-team@ztl-local-plugins`
6. `meituan-ops-team@ztl-local-plugins`
7. `supply-chain-team@ztl-local-plugins`
8. `admin-team@ztl-local-plugins`

## When to Use

- **After plugin configuration changes** - Verify changes applied correctly
- **Before major operations** - Ensure all agents are available
- **Troubleshooting** - Identify missing or misconfigured plugins
- **System startup** - Health check before multi-agent orchestration
- **Documentation** - Generate current system inventory

## Integration

This skill uses the Python execution engine in `scripts/verify_plugins_core.py`, which:
- Provides colored terminal output for readability
- Returns structured data for programmatic use
- Exit code 0 on success, 1 on issues detected

Can be integrated with:
- CI/CD pipelines (pre-deployment checks)
- Startup validation scripts
- Monitoring dashboards
- Health check endpoints
