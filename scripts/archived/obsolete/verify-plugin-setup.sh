#!/bin/bash

# ============================================
# ZTL Plugin Setup Verification Script
# ============================================
# This script verifies that all plugin configurations
# are properly set up and ready for Claude Code.
#
# Usage: bash scripts/verify-plugin-setup.sh
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}ZTL Plugin Setup Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Counter for issues
ISSUES=0
WARNINGS=0

# ============================================
# 1. Check marketplace.json
# ============================================
echo -e "${BLUE}[1/6] Checking marketplace.json...${NC}"

if [ -f ".claude-plugin/marketplace.json" ]; then
    echo -e "  ${GREEN}✓${NC} marketplace.json exists"

    # Validate JSON syntax
    if python3 -m json.tool .claude-plugin/marketplace.json > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} JSON syntax is valid"

        # Count registered plugins
        PLUGIN_COUNT=$(python3 -c "import json; print(len(json.load(open('.claude-plugin/marketplace.json'))['plugins']))" 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✓${NC} $PLUGIN_COUNT plugins registered"
    else
        echo -e "  ${RED}✗${NC} JSON syntax error in marketplace.json"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo -e "  ${RED}✗${NC} marketplace.json not found"
    echo -e "  ${YELLOW}→${NC} Expected at: .claude-plugin/marketplace.json"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# ============================================
# 2. Check settings.json
# ============================================
echo -e "${BLUE}[2/6] Checking .claude/settings.json...${NC}"

if [ -f ".claude/settings.json" ]; then
    echo -e "  ${GREEN}✓${NC} settings.json exists"

    # Check if enabledPlugins exists
    if grep -q "enabledPlugins" .claude/settings.json; then
        echo -e "  ${GREEN}✓${NC} enabledPlugins configuration found"

        # Count enabled plugins
        ENABLED_COUNT=$(python3 -c "import json; config=json.load(open('.claude/settings.json')); print(len([k for k,v in config.get('enabledPlugins',{}).items() if v==True]))" 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✓${NC} $ENABLED_COUNT plugins enabled"
    else
        echo -e "  ${YELLOW}⚠${NC} enabledPlugins not configured"
        echo -e "  ${YELLOW}→${NC} Plugins will not be active"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Check if extraKnownMarketplaces exists
    if grep -q "extraKnownMarketplaces" .claude/settings.json; then
        echo -e "  ${GREEN}✓${NC} extraKnownMarketplaces configured"
    else
        echo -e "  ${YELLOW}⚠${NC} extraKnownMarketplaces not configured"
        echo -e "  ${YELLOW}→${NC} Local marketplace won't be loaded"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "  ${RED}✗${NC} settings.json not found"
    echo -e "  ${YELLOW}→${NC} Expected at: .claude/settings.json"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# ============================================
# 3. Check plugin directory structure
# ============================================
echo -e "${BLUE}[3/6] Checking plugin directory structure...${NC}"

PLUGIN_DIRS=(
    "plugins/战略组"
    "plugins/创意组"
    "plugins/情报组"
    "plugins/筹建组"
    "plugins/开发组"
    "plugins/美团组"
    "plugins/供应组"
    "plugins/行政组"
)

VALID_PLUGINS=0
INVALID_PLUGINS=0

for plugin_dir in "${PLUGIN_DIRS[@]}"; do
    plugin_name=$(basename "$plugin_dir")

    if [ -d "$plugin_dir" ]; then
        # Check required files
        HAS_PLUGIN_JSON=false
        HAS_CORRECT_STRUCTURE=true

        if [ -f "$plugin_dir/.claude-plugin/plugin.json" ]; then
            HAS_PLUGIN_JSON=true
        else
            HAS_CORRECT_STRUCTURE=false
        fi

        # Check if directories are at root level (not inside .claude-plugin)
        if [ -d "$plugin_dir/.claude-plugin/agents" ] || \
           [ -d "$plugin_dir/.claude-plugin/commands" ] || \
           [ -d "$plugin_dir/.claude-plugin/skills" ]; then
            echo -e "  ${RED}✗${NC} $plugin_name: agents/commands/skills inside .claude-plugin (should be at root)"
            HAS_CORRECT_STRUCTURE=false
            INVALID_PLUGINS=$((INVALID_PLUGINS + 1))
        fi

        if [ "$HAS_PLUGIN_JSON" = true ] && [ "$HAS_CORRECT_STRUCTURE" = true ]; then
            VALID_PLUGINS=$((VALID_PLUGINS + 1))
        elif [ "$HAS_PLUGIN_JSON" = false ]; then
            echo -e "  ${RED}✗${NC} $plugin_name: Missing plugin.json"
            INVALID_PLUGINS=$((INVALID_PLUGINS + 1))
        fi
    else
        echo -e "  ${RED}✗${NC} $plugin_name: Directory not found"
        INVALID_PLUGINS=$((INVALID_PLUGINS + 1))
    fi
done

if [ $INVALID_PLUGINS -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} All $VALID_PLUGINS plugins have correct structure"
else
    echo -e "  ${RED}✗${NC} $INVALID_PLUGINS plugins have issues"
    ISSUES=$((ISSUES + INVALID_PLUGINS))
fi
echo ""

# ============================================
# 4. Check .mcp.json files
# ============================================
echo -e "${BLUE}[4/6] Checking .mcp.json files...${NC}"

MISSING_MCP=0
for plugin_dir in "${PLUGIN_DIRS[@]}"; do
    plugin_name=$(basename "$plugin_dir")

    if [ -f "$plugin_dir/.mcp.json" ]; then
        # Validate JSON syntax
        if python3 -m json.tool "$plugin_dir/.mcp.json" > /dev/null 2>&1; then
            : # Valid, do nothing
        else
            echo -e "  ${RED}✗${NC} $plugin_name: Invalid .mcp.json syntax"
            ISSUES=$((ISSUES + 1))
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} $plugin_name: Missing .mcp.json (declared in plugin.json)"
        MISSING_MCP=$((MISSING_MCP + 1))
    fi
done

if [ $MISSING_MCP -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} All plugins have .mcp.json files"
else
    echo -e "  ${YELLOW}⚠${NC} $MISSING_MCP plugins missing .mcp.json"
    WARNINGS=$((WARNINGS + MISSING_MCP))
fi
echo ""

# ============================================
# 5. Check .gitignore configuration
# ============================================
echo -e "${BLUE}[5/6] Checking .gitignore privacy protection...${NC}"

if [ -f ".gitignore" ]; then
    if grep -q ".claude-plugin/marketplace.json" .gitignore; then
        echo -e "  ${GREEN}✓${NC} marketplace.json is in .gitignore (private)"
    else
        echo -e "  ${YELLOW}⚠${NC} marketplace.json not in .gitignore (will be public)"
        WARNINGS=$((WARNINGS + 1))
    fi

    if grep -q ".claude/settings.local.json" .gitignore; then
        echo -e "  ${GREEN}✓${NC} settings.local.json is in .gitignore"
    else
        echo -e "  ${YELLOW}⚠${NC} settings.local.json not in .gitignore"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "  ${YELLOW}⚠${NC} .gitignore not found"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# ============================================
# 6. Summary and Next Steps
# ============================================
echo -e "${BLUE}[6/6] Summary${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $ISSUES -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. ${YELLOW}Restart Claude Code completely${NC} (Command+Q on macOS)"
    echo -e "  2. Plugins should now be loaded automatically"
    echo -e "  3. Verify by checking available agents in Claude Code"
    echo ""
    echo -e "${BLUE}To verify plugins are loaded:${NC}"
    echo -e "  • Ask Claude: 'List all available agents'"
    echo -e "  • Use: /plugin command to see installed plugins"
    echo -e "  • Check: claude --debug output for plugin loading messages"

elif [ $ISSUES -eq 0 ]; then
    echo -e "${YELLOW}⚠ Setup complete with $WARNINGS warnings${NC}"
    echo -e "  Warnings are non-critical but should be reviewed"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. ${YELLOW}Restart Claude Code completely${NC}"
    echo -e "  2. Review warnings above"

else
    echo -e "${RED}✗ Found $ISSUES critical issues${NC}"
    [ $WARNINGS -gt 0 ] && echo -e "${YELLOW}⚠ Also found $WARNINGS warnings${NC}"
    echo ""
    echo -e "${RED}Please fix critical issues before restarting Claude Code${NC}"
fi

echo -e "${BLUE}========================================${NC}"

exit $ISSUES
