# Claude Plugin Marketplace Configuration

This directory contains the **local plugin marketplace** configuration for ZTL Digital Intelligence Operations Center.

## 📁 Files

### `marketplace.json` (Private, Not in Git)
- **Purpose**: Registers all 8 business group plugins with Claude Code
- **Privacy**: ✅ In `.gitignore` - not tracked by Git
- **Status**: ✅ Auto-generated and configured

### `marketplace.json.example` (Template, In Git)
- **Purpose**: Template for team members to copy
- **Privacy**: ✅ Safe to commit - no sensitive data
- **Usage**: Copy to `marketplace.json` if yours is missing

## 🚀 Quick Setup (New Team Member)

If you just cloned this repo and plugins aren't working:

```bash
# 1. Copy the example template
cp .claude-plugin/marketplace.json.example .claude-plugin/marketplace.json

# 2. Verify configuration
bash scripts/verify-plugin-setup.sh

# 3. Restart Claude Code (Command+Q on macOS)
```

## 🔒 Privacy Notice

`marketplace.json` is **intentionally excluded from Git** because:
- Each developer may have different local paths
- Personal plugin preferences should not be forced on team
- Allows flexibility in plugin activation

The actual **plugin definitions** (in `plugins/*/`) are fully tracked by Git.

## 📚 Learn More

See [PLUGIN-SETUP-GUIDE.md](../PLUGIN-SETUP-GUIDE.md) for complete documentation.
