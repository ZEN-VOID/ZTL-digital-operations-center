---
name: plugins
description: Comprehensive guide for creating professional Claude Code plugins with standardized structure, including commands, agents, skills, hooks, and MCP integrations. Use when building distributable plugin packages or understanding plugin architecture.
---

# Claude Code Plugin Creation

Build production-ready, distributable Claude Code plugins that extend functionality through standardized packaging of commands, agents, skills, hooks, and MCP servers.

## What Are Plugins?

Plugins are self-contained packages that extend Claude Code's capabilities through a standardized structure. Each plugin:

- ✅ Packages **multiple component types** (commands, agents, skills, hooks, MCP servers)
- ✅ Uses **plugin.json manifest** for metadata and configuration
- ✅ Supports **custom paths** for flexible organization
- ✅ Enables **distribution and reuse** across teams and projects
- ✅ Provides **automatic discovery** of all components

**Key Benefits**:
- **Modularity**: Bundle related functionality into cohesive packages
- **Distribution**: Share plugins via Git, npm, or direct downloads
- **Team Collaboration**: Standardize workflows and tools across teams
- **Versioning**: Track changes with semantic versioning
- **Discoverability**: Automatic component registration

## When to Use This Skill

Use this skill to:

- Create distributable plugin packages for Claude Code
- Understand plugin architecture and best practices
- Package multiple related components (commands, agents, skills)
- Build team or company-wide standardization tools
- Design plugin directory structures and configurations
- Integrate MCP servers into plugins
- Debug plugin loading and component registration

## Plugin Architecture

### Complete Plugin Structure

```yaml
enterprise-plugin/
├── .claude-plugin/           # 📋 Metadata Directory (Required)
│   └── plugin.json          # Plugin manifest with name, version, author, paths
│
├── commands/                 # 🔧 Default Commands Location
│   ├── status.md            # Slash command for status checking
│   └── logs.md              # Slash command for log viewing
│
├── agents/                   # 🤖 Default Agents Location
│   ├── security-reviewer.md # Subagent for security review
│   ├── performance-tester.md # Subagent for performance testing
│   └── compliance-checker.md # Subagent for compliance validation
│
├── skills/                   # 🎯 Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
│
├── hooks/                    # 🔗 Event Hooks
│   ├── hooks.json           # Main hooks configuration
│   └── security-hooks.json  # Additional hooks
│
├── .mcp.json                # 🌐 MCP Server Definitions
│
├── scripts/                 # 📜 Hook & Utility Scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
│
├── LICENSE                  # ⚖️ License File
└── CHANGELOG.md             # 📝 Version History

Key Concepts:
  - .claude-plugin/: Must contain plugin.json manifest
  - Default directories: commands/, agents/, skills/, hooks/
  - Custom paths: Can be configured in plugin.json
  - All paths relative: Must start with ./
  - Supplemental structure: Custom paths supplement, don't replace defaults
```

### Component Layers

```yaml
Layer 1 - Metadata:
  Location: .claude-plugin/plugin.json
  Purpose: Plugin identification, versioning, configuration
  Required: name, version, description, author

Layer 2 - Commands:
  Location: commands/ (default) or custom path
  Purpose: Slash command definitions
  Integration: Automatic registration in /help

Layer 3 - Agents:
  Location: agents/ (default) or custom path
  Purpose: Specialized subagent configurations
  Integration: Auto-delegation based on descriptions

Layer 4 - Skills:
  Location: skills/ (default) or custom path
  Purpose: Modular capabilities with resources
  Integration: Auto-discovery based on SKILL.md

Layer 5 - Hooks:
  Location: hooks/ (default) or custom path
  Purpose: Event-driven automation
  Integration: Lifecycle event handlers

Layer 6 - MCP Servers:
  Location: .mcp.json
  Purpose: External tool integrations
  Integration: Auto-launch when plugin enables
```

## Quick Start

### 1. Plan Plugin Scope

Answer these core questions:

```yaml
Plugin Goal: What problem does this plugin solve?
Target Users: Who will use this plugin? (Team/Company/Community)
Value Proposition: What unique value does it provide?

Component Checklist:
  Commands:
    - [ ] What frequent workflows need shortcuts?
    - [ ] Which commands need parameters?
    - [ ] Any Bash execution requirements?

  Agents:
    - [ ] What specialized roles needed?
    - [ ] Which tools should each agent access?
    - [ ] Any inter-agent collaboration patterns?

  Skills:
    - [ ] What complex workflows to automate?
    - [ ] Which skills need scripts/references?
    - [ ] Any shared utility skills?

  Hooks:
    - [ ] What events to automate?
    - [ ] Any validation/blocking requirements?
    - [ ] Any post-operation processing?

  MCP Servers:
    - [ ] What external services to integrate?
    - [ ] Any authentication requirements?
    - [ ] Resource access patterns?
```

### 2. Initialize Plugin Structure

Use the provided initialization script:

```bash
# Run plugin initialization script
python3 .claude/skills/元skills/plugins/scripts/init_plugin.py \
  --name "enterprise-plugin" \
  --description "Enterprise development toolkit" \
  --author "Your Team" \
  --output "./my-plugins"

# This creates:
# my-plugins/enterprise-plugin/
#   ├── .claude-plugin/plugin.json
#   ├── commands/
#   ├── agents/
#   ├── skills/
#   ├── hooks/
#   ├── scripts/
#   ├── LICENSE
#   ├── CHANGELOG.md
#   └── README.md
```

### 3. Create plugin.json Manifest

The manifest defines plugin metadata and configuration:

```json
{
  "name": "enterprise-plugin",
  "version": "1.0.0",
  "description": "Enterprise development toolkit with security, performance, and compliance tools",
  "author": {
    "name": "Your Team",
    "email": "team@company.com",
    "url": "https://github.com/yourteam"
  },
  "homepage": "https://github.com/yourteam/enterprise-plugin",
  "repository": "https://github.com/yourteam/enterprise-plugin",
  "license": "MIT",
  "keywords": ["security", "performance", "compliance", "enterprise"],

  "commands": "./commands",
  "agents": "./agents",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Required Fields**:
- `name`: Unique identifier in kebab-case
- `version`: Semantic versioning (MAJOR.MINOR.PATCH)
- `description`: Brief purpose statement
- `author`: Object with name, email, and URL

**Optional Fields**:
- `homepage`: Documentation URL
- `repository`: Source code repository link
- `license`: License identifier (MIT, Apache-2.0, etc.)
- `keywords`: Array of discovery tags
- `commands`, `agents`, `hooks`, `mcpServers`: Custom paths

### 4. Build Plugin Components

#### Create Commands

**Leverage existing commands skill**:

```bash
# Use the commands meta-skill to create slash commands
# Reference: .claude/skills/元skills/commands/

Example command structure:
  commands/
    ├── security-scan.md
    ├── performance-test.md
    └── deploy.md

Each command follows standard format:
  ---
  description: Brief command description
  argument-hint: [optional parameters]
  allowed-tools: Tool1, Tool2
  ---

  # Command Content
  [Your prompt content here]
```

**Refer to commands meta-skill** for detailed command creation guidance.

#### Create Agents

**Leverage existing agents skill**:

```bash
# Use the agents meta-skill to create subagents
# Reference: .claude/skills/元skills/agents/

Example agent structure:
  agents/
    ├── security-reviewer.md
    ├── performance-tester.md
    └── compliance-checker.md

Each agent follows standard format:
  ---
  name: agent-name
  description: When this agent should be invoked
  tools: Tool1, Tool2, Tool3
  model: sonnet
  ---

  # Agent System Prompt
  [Role definition, capabilities, examples]
```

**Refer to agents meta-skill** for detailed agent creation guidance including:
- 10-element prompt system
- Context engineering principles
- Skills integration patterns
- Tool configuration strategies

#### Create Skills

**Leverage existing skill-creator skill**:

```bash
# Use the skill-creator meta-skill to create skills
# Reference: .claude/skills/元skills/skills/

Example skill structure:
  skills/
    ├── code-reviewer/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── analyze_complexity.py
    │   └── references/
    │       └── style_guide.md
    └── pdf-processor/
        ├── SKILL.md
        └── scripts/
            └── process_pdf.py

Each skill follows standard format:
  ---
  name: skill-name
  description: What this skill does and when to use it
  ---

  # Skill Content
  [Usage instructions, API reference, examples]
```

**Refer to skill-creator meta-skill** for detailed skill creation guidance including:
- Progressive disclosure design
- Bundled resources organization
- Step-by-step creation process

#### Create Hooks

**Leverage existing hooks skill**:

```bash
# Use the hooks meta-skill to create event hooks
# Reference: .claude/skills/元skills/hooks/

Example hook structure:
  hooks/
    ├── hooks.json
    └── security-hooks.json

  scripts/
    ├── block-dangerous-commands.sh
    ├── auto-format.sh
    └── security-scan.py

hooks.json format:
  {
    "hooks": {
      "PreToolUse": [{
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "./scripts/block-dangerous-commands.sh",
          "description": "Block dangerous bash commands"
        }]
      }],
      "PostToolUse": [{
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "./scripts/auto-format.sh",
          "description": "Auto-format after edit"
        }]
      }]
    }
  }
```

**Refer to hooks meta-skill** for detailed hook creation guidance including:
- 8 lifecycle event types
- Cross-platform script development
- Testing and debugging strategies

#### Configure MCP Servers

MCP servers provide external tool integrations:

```json
{
  "mcpServers": {
    "security-scanner": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/security-mcp-server.js"],
      "env": {
        "API_KEY": "${SECURITY_API_KEY}",
        "LOG_LEVEL": "info"
      }
    },
    "performance-analyzer": {
      "type": "stdio",
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/performance-mcp-server.py"],
      "env": {
        "METRICS_DB": "${HOME}/.claude/metrics.db"
      }
    }
  }
}
```

**Key Concepts**:
- `${CLAUDE_PLUGIN_ROOT}`: References plugin directory path
- `type`: Connection type (stdio, sse, websocket)
- `command`: Executable to launch
- `args`: Command-line arguments
- `env`: Environment variables

### 5. Test Plugin

#### Local Testing

```bash
# 1. Copy plugin to test location
cp -r ./enterprise-plugin ~/.claude/plugins/

# 2. Create test configuration
cat > .claude/settings.json <<'EOF'
{
  "enabledPlugins": ["enterprise-plugin"]
}
EOF

# 3. Restart Claude Code
# (Complete exit and restart required)

# 4. Verify plugin loading
claude --debug

# Check for:
# - "Loading plugin: enterprise-plugin"
# - "Registered N commands"
# - "Registered N agents"
# - "Registered N skills"
```

#### Component Verification

```yaml
Commands Verification:
  1. Run /help to see registered commands
  2. Test each command with sample inputs
  3. Verify parameter substitution works
  4. Check tool permissions respected

Agents Verification:
  1. Check /agents to see registered agents
  2. Explicitly invoke each agent
  3. Test auto-delegation functionality
  4. Verify tool access restrictions

Skills Verification:
  1. Trigger skills through agent invocation
  2. Test bundled scripts execution
  3. Verify references loading
  4. Check assets accessibility

Hooks Verification:
  1. Trigger relevant events
  2. Check hook scripts execute
  3. Verify blocking behavior (PreToolUse)
  4. Review log outputs

MCP Servers Verification:
  1. Check server process launched
  2. Test tool calls
  3. Verify authentication
  4. Check error handling
```

### 6. Package and Distribute

#### Create Distribution Package

```bash
# Use packaging script
python3 .claude/skills/元skills/plugins/scripts/package_plugin.py \
  ./enterprise-plugin \
  --output ./dist

# This creates:
# dist/enterprise-plugin-1.0.0.zip
#   - Validated plugin structure
#   - Includes all components
#   - Ready for distribution
```

#### Distribution Methods

```yaml
Method 1 - Git Repository:
  1. Push plugin to GitHub/GitLab
  2. Tag releases with versions
  3. Users clone repository:
     git clone https://github.com/yourteam/enterprise-plugin
     cp -r enterprise-plugin ~/.claude/plugins/

Method 2 - NPM Package:
  1. Create package.json
  2. Publish to npm registry
  3. Users install via npm:
     npm install -g @yourteam/claude-enterprise-plugin

Method 3 - Direct Download:
  1. Upload zip to releases page
  2. Users download and extract
  3. Copy to plugins directory

Method 4 - Private Registry:
  1. Host on internal server
  2. Provide installation script
  3. Automatic updates via CI/CD
```

#### Installation Instructions

```markdown
# Installation

## Method 1: Git Clone

```bash
git clone https://github.com/yourteam/enterprise-plugin
cp -r enterprise-plugin ~/.claude/plugins/
```

## Method 2: Download Release

1. Download latest release from [Releases](https://github.com/yourteam/enterprise-plugin/releases)
2. Extract zip file
3. Copy to `~/.claude/plugins/`

## Configuration

Add to your `.claude/settings.json`:

```json
{
  "enabledPlugins": ["enterprise-plugin"]
}
```

## Restart Required

Completely exit and restart Claude Code for plugin to load.
```

## Advanced Topics

### Custom Path Configuration

Override default component paths in plugin.json:

```json
{
  "name": "custom-structure-plugin",
  "version": "1.0.0",

  "commands": "./src/commands",
  "agents": "./src/agents",
  "hooks": "./config/hooks.json",
  "mcpServers": "./config/mcp.json"
}
```

**Rules**:
- All paths must be relative
- All paths must start with `./`
- Custom paths **supplement** default directories
- Components in both default and custom paths both load

### Environment Variables

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/server.js"],
      "env": {
        "DATA_DIR": "${CLAUDE_PLUGIN_ROOT}/data",
        "CONFIG": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

**Available Variables**:
- `${CLAUDE_PLUGIN_ROOT}`: Plugin installation directory
- `${HOME}`: User home directory
- `${CWD}`: Current working directory
- Custom environment variables from shell

### Multi-Component Coordination

Design patterns for component interaction:

```yaml
Pattern 1: Command → Agent → Skill
  Flow: /deploy → deploy-agent → deployment-skill
  Use: Complex workflows with orchestration

Pattern 2: Hook → Agent
  Flow: PostToolUse → code-review-agent
  Use: Automatic quality checks

Pattern 3: Agent → Multiple Skills
  Flow: analysis-agent → [data-skill, chart-skill, report-skill]
  Use: Multi-step analysis workflows

Pattern 4: Multiple Agents → Shared Skill
  Flow: [agent-A, agent-B, agent-C] → common-utility-skill
  Use: Reusable utilities
```

### Version Management

Follow semantic versioning:

```yaml
Version Format: MAJOR.MINOR.PATCH

Increment Rules:
  MAJOR: Breaking changes (incompatible API changes)
  MINOR: New features (backward-compatible additions)
  PATCH: Bug fixes (backward-compatible fixes)

Examples:
  1.0.0 → 1.0.1: Bug fix
  1.0.1 → 1.1.0: New command added
  1.1.0 → 2.0.0: Changed agent interface

CHANGELOG.md Template:
  # Changelog

  ## [1.1.0] - 2025-01-20
  ### Added
  - New security-scan command
  - Performance testing agent

  ### Fixed
  - Hook script permissions issue

  ## [1.0.0] - 2025-01-15
  ### Added
  - Initial release
  - Security review agent
  - Code formatting hooks
```

## Plugin Examples

### Example 1: Security Plugin

**Structure**:
```
security-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── scan.md
│   └── audit.md
├── agents/
│   ├── security-reviewer.md
│   └── vulnerability-scanner.md
├── skills/
│   └── security-analysis/
│       ├── SKILL.md
│       └── scripts/
│           ├── scan_dependencies.py
│           └── check_secrets.py
├── hooks/
│   └── hooks.json
├── scripts/
│   ├── block-dangerous-ops.sh
│   └── scan-on-commit.sh
└── LICENSE
```

**plugin.json**:
```json
{
  "name": "security-plugin",
  "version": "1.0.0",
  "description": "Comprehensive security toolkit for code analysis and vulnerability detection",
  "author": {
    "name": "Security Team",
    "email": "security@company.com"
  },
  "keywords": ["security", "vulnerability", "audit"],
  "license": "MIT"
}
```

### Example 2: Data Analysis Plugin

**Structure**:
```
data-analysis-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── analyze.md
│   └── visualize.md
├── agents/
│   ├── data-scientist.md
│   └── statistician.md
├── skills/
│   ├── data-pipeline/
│   │   ├── SKILL.md
│   │   └── scripts/
│   └── chart-generator/
│       ├── SKILL.md
│       ├── scripts/
│       └── assets/templates/
└── .mcp.json (database connections)
```

### Example 3: DevOps Plugin

**Structure**:
```
devops-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy.md
│   ├── rollback.md
│   └── status.md
├── agents/
│   ├── deployment-manager.md
│   ├── infrastructure-engineer.md
│   └── monitoring-specialist.md
├── skills/
│   └── kubernetes-ops/
│       ├── SKILL.md
│       └── scripts/
├── hooks/
│   └── hooks.json
├── scripts/
│   ├── pre-deploy-checks.sh
│   └── post-deploy-verify.sh
└── .mcp.json (k8s, AWS, monitoring tools)
```

## Quality Checklist

```yaml
□ Plugin Metadata
  - [ ] plugin.json format correct
  - [ ] All required fields present (name, version, description, author)
  - [ ] Version follows semantic versioning
  - [ ] Keywords descriptive and relevant
  - [ ] License specified

□ Directory Structure
  - [ ] .claude-plugin/ directory exists
  - [ ] Component directories organized logically
  - [ ] Custom paths (if any) configured correctly
  - [ ] All paths relative and start with ./

□ Components Quality
  - [ ] Commands follow standard format (see commands meta-skill)
  - [ ] Agents follow 10-element prompt system (see agents meta-skill)
  - [ ] Skills follow progressive disclosure (see skill-creator meta-skill)
  - [ ] Hooks follow event-driven patterns (see hooks meta-skill)
  - [ ] MCP servers configured with proper paths

□ Testing Completeness
  - [ ] All commands tested with sample inputs
  - [ ] All agents verified for auto-delegation
  - [ ] All skills triggered successfully
  - [ ] All hooks fire on correct events
  - [ ] MCP servers launch and respond

□ Documentation
  - [ ] README.md with installation instructions
  - [ ] CHANGELOG.md with version history
  - [ ] LICENSE file present
  - [ ] Component usage examples
  - [ ] Troubleshooting guide

□ Distribution Ready
  - [ ] Plugin validates without errors
  - [ ] Package created successfully
  - [ ] Installation tested on clean system
  - [ ] Repository/registry published
```

## Best Practices

### 1. Follow Single Responsibility Principle

Each plugin should have a **clear, focused purpose**:

✅ Good:
- `security-plugin`: Security analysis and vulnerability detection
- `data-plugin`: Data analysis and visualization
- `devops-plugin`: Deployment and infrastructure management

❌ Bad:
- `everything-plugin`: Tries to do too many unrelated things
- `utils-plugin`: Vague, unfocused collection

### 2. Design for Reusability

Components should be **modular and composable**:

```yaml
Reusable Skills:
  - Create agent-agnostic skills
  - Skills should work with multiple agents
  - Avoid hardcoded agent-specific logic

Shared Commands:
  - Commands should be self-contained
  - Use parameters for flexibility
  - Don't assume specific project structure

Universal Hooks:
  - Hooks should be configurable
  - Avoid project-specific paths
  - Use environment variables
```

### 3. Provide Clear Documentation

Every plugin needs comprehensive docs:

```markdown
Required Documentation:
  - README.md: Installation, usage, examples
  - CHANGELOG.md: Version history
  - LICENSE: Usage rights
  - Component docs: Each agent/skill/command documented

Optional Documentation:
  - CONTRIBUTING.md: Contribution guidelines
  - ARCHITECTURE.md: Design decisions
  - TROUBLESHOOTING.md: Common issues
```

### 4. Version Responsibly

Follow semantic versioning strictly:

```yaml
Breaking Changes (MAJOR):
  - Changed command interface
  - Removed/renamed agents
  - Modified skill APIs
  - Changed hook signatures

New Features (MINOR):
  - Added new commands
  - Added new agents/skills
  - Enhanced existing components
  - New MCP integrations

Bug Fixes (PATCH):
  - Fixed broken functionality
  - Corrected documentation
  - Updated dependencies
```

### 5. Test Thoroughly

Comprehensive testing strategy:

```yaml
Unit Testing:
  - Test commands individually
  - Test agents with various inputs
  - Test skills in isolation
  - Test hooks with mock events

Integration Testing:
  - Test command → agent → skill flows
  - Test hook → agent interactions
  - Test MCP server connections

System Testing:
  - Test on clean install
  - Test with other plugins
  - Test across platforms
  - Test upgrade paths
```

## Debugging

### Plugin Not Loading

```yaml
Symptoms:
  - Plugin doesn't appear in enabled list
  - Components not registered
  - No error messages

Diagnosis:
  1. Check plugin.json syntax:
     cat .claude/plugins/your-plugin/.claude-plugin/plugin.json | jq .

  2. Verify directory structure:
     ls -la .claude/plugins/your-plugin/

  3. Check settings.json:
     cat .claude/settings.json | jq '.enabledPlugins'

  4. Run with debug mode:
     claude --debug

  5. Check Claude Code logs

Solutions:
  - Ensure .claude-plugin/ directory exists
  - Verify plugin.json is valid JSON
  - Restart Claude Code completely
  - Check file permissions
```

### Components Not Registering

```yaml
Symptoms:
  - Plugin loads but components missing
  - Commands don't appear in /help
  - Agents not in /agents list

Diagnosis:
  1. Verify component paths in plugin.json
  2. Check component file formats
  3. Validate YAML frontmatter
  4. Review debug output

Solutions:
  - Ensure paths are relative and start with ./
  - Check YAML frontmatter syntax
  - Verify required fields present
  - Review component naming conventions
```

### MCP Servers Not Starting

```yaml
Symptoms:
  - MCP tools unavailable
  - Server process not running
  - Connection errors

Diagnosis:
  1. Check .mcp.json syntax
  2. Verify script paths
  3. Check environment variables
  4. Review server logs

Solutions:
  - Use ${CLAUDE_PLUGIN_ROOT} for paths
  - Ensure scripts are executable
  - Validate environment variable names
  - Check server implementation
```

## Reference Resources

### Official Documentation

- **[Claude Code Plugins Reference](https://docs.claude.com/zh-CN/docs/claude-code/plugins-reference)** ⭐ Must-read
- [Claude Code Commands](https://docs.claude.com/zh-CN/docs/claude-code/slash-commands)
- [Claude Code Subagents](https://docs.claude.com/zh-CN/docs/claude-code/sub-agents)
- [Claude Code Skills](https://docs.claude.com/zh-CN/docs/claude-code/skills)
- [Claude Code Hooks](https://docs.claude.com/zh-CN/docs/claude-code/hooks)
- [MCP Documentation](https://modelcontextprotocol.io)

### Related Meta-Skills

This skill integrates with other meta-skills for component creation:

- **commands**: Use for creating slash commands (`.claude/skills/元skills/commands/`)
- **agents**: Use for creating subagents (`.claude/skills/元skills/agents/`)
- **skill-creator**: Use for creating skills (`.claude/skills/元skills/skills/`)
- **hooks**: Use for creating event hooks (`.claude/skills/元skills/hooks/`)

### Community Resources

- [Claude Code GitHub Discussions](https://github.com/anthropics/claude-code/discussions)
- [Example Plugins Repository](https://github.com/anthropics/claude-code-plugins)
- [Plugin Development Guide](https://docs.claude.com/plugins/development)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-28
**Compatibility**: Claude Code v1.0.124+
**Based On**: Claude Code Official Documentation (2025-10-23)
