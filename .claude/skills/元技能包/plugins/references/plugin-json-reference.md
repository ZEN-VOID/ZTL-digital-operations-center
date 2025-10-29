# plugin.json Complete Reference

Complete specification for the `plugin.json` manifest file.

## Location

```
.claude-plugin/plugin.json
```

**Required**: This file must exist at this exact path.

## Complete Schema

```json
{
  "name": "string (required)",
  "version": "string (required)",
  "description": "string (required)",
  "author": {
    "name": "string (required)",
    "email": "string (optional)",
    "url": "string (optional)"
  },
  "homepage": "string (optional)",
  "repository": "string (optional)",
  "license": "string (optional)",
  "keywords": ["string", "..."] (optional),

  "commands": "string (optional)",
  "agents": "string (optional)",
  "hooks": "string (optional)",
  "mcpServers": "string (optional)"
}
```

## Field Specifications

### name (required)

- **Type**: `string`
- **Format**: kebab-case (lowercase with hyphens)
- **Purpose**: Unique identifier for the plugin
- **Rules**:
  - Must be lowercase
  - Must use hyphens for word separation
  - No spaces allowed
  - Must be unique across all installed plugins

**Examples**:
```json
✅ "enterprise-plugin"
✅ "security-toolkit"
✅ "data-analysis-tools"

❌ "EnterprisePlugin" (not lowercase)
❌ "enterprise_plugin" (underscores)
❌ "enterprise plugin" (spaces)
```

### version (required)

- **Type**: `string`
- **Format**: Semantic Versioning (MAJOR.MINOR.PATCH)
- **Purpose**: Track plugin versions for compatibility and updates

**Rules**:
- MAJOR: Increment for breaking changes
- MINOR: Increment for new features (backward-compatible)
- PATCH: Increment for bug fixes (backward-compatible)

**Examples**:
```json
✅ "1.0.0"
✅ "2.3.1"
✅ "0.1.0" (pre-release)

❌ "1.0" (missing patch)
❌ "v1.0.0" (no 'v' prefix)
❌ "1.0.0-beta" (use MINOR=0 for pre-release)
```

### description (required)

- **Type**: `string`
- **Purpose**: Brief explanation of plugin's purpose
- **Guidelines**:
  - One sentence preferred
  - Focus on value proposition
  - Avoid technical jargon
  - Be specific about what it does

**Examples**:
```json
✅ "Enterprise development toolkit with security, performance, and compliance tools"
✅ "Data analysis and visualization suite for business intelligence"
✅ "Automated security scanning and vulnerability detection"

❌ "A plugin" (too vague)
❌ "Does stuff" (not specific)
❌ "The best plugin ever created..." (marketing fluff)
```

### author (required)

- **Type**: `object`
- **Purpose**: Identify plugin creator/maintainer

**Structure**:
```json
{
  "name": "string (required)",
  "email": "string (optional)",
  "url": "string (optional)"
}
```

**Examples**:
```json
✅ {
  "name": "Security Team",
  "email": "security@company.com",
  "url": "https://github.com/company-security"
}

✅ {
  "name": "John Doe"
}

❌ "John Doe" (must be object, not string)
```

### homepage (optional)

- **Type**: `string`
- **Format**: Valid URL
- **Purpose**: Link to plugin documentation

**Examples**:
```json
✅ "https://github.com/yourteam/enterprise-plugin"
✅ "https://plugins.yourcompany.com/enterprise"
✅ "https://docs.yourcompany.com/plugins/enterprise"
```

### repository (optional)

- **Type**: `string`
- **Format**: Valid URL or Git URL
- **Purpose**: Link to source code repository

**Examples**:
```json
✅ "https://github.com/yourteam/enterprise-plugin"
✅ "git@github.com:yourteam/enterprise-plugin.git"
✅ "https://gitlab.com/yourteam/enterprise-plugin"
```

### license (optional)

- **Type**: `string`
- **Format**: SPDX License Identifier
- **Purpose**: Specify usage rights

**Common Values**:
```json
"MIT"
"Apache-2.0"
"GPL-3.0"
"BSD-3-Clause"
"ISC"
"Proprietary"
```

### keywords (optional)

- **Type**: `array of strings`
- **Purpose**: Help with plugin discovery and search

**Guidelines**:
- Use 3-7 keywords
- Be specific
- Include domain terms
- Include use cases

**Examples**:
```json
✅ ["security", "vulnerability", "audit", "compliance"]
✅ ["data", "analysis", "visualization", "charts"]
✅ ["devops", "deployment", "kubernetes", "ci-cd"]

❌ ["plugin", "tool"] (too generic)
❌ ["awesome", "best"] (subjective)
```

## Custom Path Configuration

Override default component locations.

### commands (optional)

- **Type**: `string`
- **Purpose**: Custom path to commands directory
- **Default**: `./commands`

**Rules**:
- Must be relative path
- Must start with `./`
- Supplements default directory (doesn't replace)

**Examples**:
```json
✅ "./src/commands"
✅ "./cli/commands"

❌ "src/commands" (missing ./)
❌ "/absolute/path" (absolute path)
```

### agents (optional)

- **Type**: `string`
- **Purpose**: Custom path to agents directory
- **Default**: `./agents`

**Examples**:
```json
✅ "./src/agents"
✅ "./ai/agents"
```

### hooks (optional)

- **Type**: `string`
- **Purpose**: Custom path to hooks configuration
- **Default**: `./hooks/hooks.json`

**Examples**:
```json
✅ "./config/hooks.json"
✅ "./hooks/main.json"
```

### mcpServers (optional)

- **Type**: `string`
- **Purpose**: Custom path to MCP servers configuration
- **Default**: `./.mcp.json`

**Examples**:
```json
✅ "./config/mcp.json"
✅ "./mcp-servers.json"
```

## Complete Examples

### Minimal Plugin

```json
{
  "name": "simple-plugin",
  "version": "1.0.0",
  "description": "A simple plugin example",
  "author": {
    "name": "Your Name"
  }
}
```

### Full-Featured Plugin

```json
{
  "name": "enterprise-plugin",
  "version": "2.3.1",
  "description": "Enterprise development toolkit with security, performance, and compliance tools",
  "author": {
    "name": "Enterprise Team",
    "email": "team@company.com",
    "url": "https://github.com/company/enterprise-team"
  },
  "homepage": "https://company.com/plugins/enterprise",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "Apache-2.0",
  "keywords": [
    "security",
    "performance",
    "compliance",
    "enterprise",
    "devops"
  ],

  "commands": "./src/commands",
  "agents": "./src/agents",
  "hooks": "./config/hooks.json",
  "mcpServers": "./config/mcp.json"
}
```

### Open Source Plugin

```json
{
  "name": "community-tools",
  "version": "1.5.0",
  "description": "Community-contributed development tools and utilities",
  "author": {
    "name": "Open Source Community",
    "url": "https://github.com/claude-community/tools"
  },
  "homepage": "https://claude-community.github.io/tools",
  "repository": "https://github.com/claude-community/tools",
  "license": "MIT",
  "keywords": [
    "community",
    "tools",
    "utilities",
    "open-source"
  ]
}
```

### Internal Company Plugin

```json
{
  "name": "acme-corp-standards",
  "version": "3.2.0",
  "description": "ACME Corp internal standards and workflows",
  "author": {
    "name": "ACME Engineering",
    "email": "engineering@acme.corp"
  },
  "homepage": "https://internal.acme.corp/plugins/standards",
  "repository": "git@github.acme.corp:engineering/standards-plugin.git",
  "license": "Proprietary",
  "keywords": [
    "acme",
    "standards",
    "internal",
    "workflows"
  ]
}
```

## Validation

### Required Field Validation

```python
def validate_plugin_json(data):
    required_fields = ["name", "version", "description", "author"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate author structure
    if not isinstance(data["author"], dict):
        raise ValueError("author must be an object")

    if "name" not in data["author"]:
        raise ValueError("author.name is required")
```

### Format Validation

```python
import re

def validate_name(name):
    # Must be lowercase with hyphens
    pattern = r'^[a-z][a-z0-9-]*$'
    if not re.match(pattern, name):
        raise ValueError(f"Invalid name format: {name}")

def validate_version(version):
    # Must be semantic version
    pattern = r'^\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        raise ValueError(f"Invalid version format: {version}")

def validate_path(path):
    # Must be relative and start with ./
    if not path.startswith('./'):
        raise ValueError(f"Path must start with ./: {path}")
```

## Best Practices

1. **Keep name short and descriptive**
   - Use 2-3 words maximum
   - Reflect plugin's purpose
   - Avoid redundant terms like "plugin" or "tool"

2. **Follow semantic versioning strictly**
   - Document breaking changes
   - Maintain CHANGELOG.md
   - Tag releases in Git

3. **Write clear descriptions**
   - One sentence is ideal
   - Focus on value, not implementation
   - Be specific about what it does

4. **Provide contact information**
   - Include email for support
   - Link to repository for issues
   - Provide documentation URL

5. **Use meaningful keywords**
   - Think about how users search
   - Include domain terms
   - Include use case terms

6. **Document custom paths**
   - Explain why custom paths are used
   - Keep structure intuitive
   - Update README to match

## Troubleshooting

### Plugin Not Loading

**Symptom**: Plugin doesn't appear in enabled list

**Check**:
1. Verify .claude-plugin/plugin.json exists
2. Validate JSON syntax: `cat plugin.json | jq .`
3. Check required fields present
4. Verify name format (kebab-case)

### Invalid JSON Error

**Symptom**: Error parsing plugin.json

**Solutions**:
- Remove trailing commas
- Use double quotes, not single
- Escape special characters
- Validate with JSON linter

### Version Conflicts

**Symptom**: Plugin version mismatch

**Solutions**:
- Update version in plugin.json
- Update CHANGELOG.md to match
- Tag Git release with version
- Communicate breaking changes

## References

- [Semantic Versioning](https://semver.org/)
- [SPDX License List](https://spdx.org/licenses/)
- [JSON Specification](https://www.json.org/)
- [Claude Code Plugin Docs](https://docs.claude.com/zh-CN/docs/claude-code/plugins-reference)
