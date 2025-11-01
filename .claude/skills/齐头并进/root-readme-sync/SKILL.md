---
name: root-readme-sync
description: Automatically synchronize root-level README.md files (project root, plugin root) by analyzing entire project structure changes from git diff, generating professional GitHub-standard documentation with project overview, architecture, features, and comprehensive navigation.
---

# Root README Sync Skill

> Intelligent root-level documentation synchronization with comprehensive project analysis

## Quick Start

**When to use**:
- After major structural changes (new plugins, new modules, reorganization)
- When project features/capabilities expand
- Periodic maintenance to ensure root docs reflect current state
- Before publishing to GitHub or sharing with team
- After completing sprint/milestone with significant changes

**Auto-invoked when**:
- User mentions "update root README", "sync project documentation", "refresh main README"
- After batch operations affecting multiple subdirectories
- When running full project documentation update
- Major version releases

**Example invocations**:
```
User: "更新项目主 README"
User: "同步 plugins/开发组/ 的 README"
User: "项目结构改了很多,更新根目录文档"
```

---

## Core Functionality

This skill provides **intelligent root README synchronization** with:

1. **Comprehensive Analysis** - Scans entire project structure, all subdirectories, all capabilities
2. **Change Detection** - Uses git diff to identify updates since last sync
3. **Professional Documentation** - GitHub-standard README with badges, architecture diagrams, feature highlights
4. **Smart Composition** - Aggregates data from all subdirectories, plugin.json, agent files
5. **Template-Driven** - Uses proven README templates (project root, plugin root have different formats)
6. **Quality Assurance** - Validates completeness, accuracy, broken links, outdated information

---

## Workflow

```
Step 1: Change Detection & Scope Analysis
├─ Use Git diff to detect changes
│  ├─ Compare HEAD with recent commits (HEAD~10..HEAD)
│  ├─ Parse changes since last root README update
│  └─ Identify affected modules/plugins
└─ Determine update scope:
   ├─ Full regeneration (major changes)
   └─ Incremental update (minor changes)

Step 2: Comprehensive Project Analysis
├─ Scan project root structure
│  ├─ Identify all plugins/modules
│  ├─ Count agents/commands/skills globally
│  └─ Extract project metadata
├─ Read existing README (if exists)
│  └─ Preserve manual sections
├─ Analyze subdirectory READMEs
│  └─ Extract summaries for aggregation
└─ Identify key features and capabilities

Step 3: Content Generation
├─ Project Overview Section
│  ├─ Project name and tagline
│  ├─ Badges (version, agents, plugins, status)
│  ├─ Brief description
│  └─ Key highlights
├─ Architecture Section
│  ├─ High-level architecture diagram (text/mermaid)
│  ├─ Plugin organization
│  └─ Agent orchestration model
├─ Features Section
│  ├─ Core capabilities
│  ├─ Plugin breakdown
│  └─ Unique selling points
├─ Quick Start Section
│  ├─ Installation
│  ├─ Basic usage
│  └─ First steps
├─ Documentation Navigation
│  ├─ Links to all plugin READMEs
│  ├─ Links to key documents
│  └─ API/command references
└─ Metadata Section
   ├─ Version info
   ├─ Requirements
   ├─ License
   └─ Contributors

Step 4: Quality Validation
├─ Verify all plugins documented
├─ Check link validity (internal paths)
├─ Validate badge URLs
├─ Ensure statistics accurate
└─ Markdown syntax check

Step 5: Output & Reporting
├─ Write updated README.md
├─ Generate update summary
├─ Log changes made
└─ Report to user with statistics
```

---

## Supported Root Types

### Type 1: Project Root README

**Location**: `/README.md`

**Purpose**: Entry point for entire ZTL Digital Intelligence Operations Center

**Structure**:
```markdown
# ZTL数智化作战中心

> AI-Powered Multi-Agent Orchestration Platform for Restaurant Industry Digital Transformation

[![Agents](https://img.shields.io/badge/agents-84+-blue)]()
[![Plugins](https://img.shields.io/badge/plugins-8-green)]()
[![Skills](https://img.shields.io/badge/skills-15+-orange)]()
[![Status](https://img.shields.io/badge/status-production-brightgreen)]()

## 📋 Project Overview

[Comprehensive description]

## 🏗️ Architecture

[Multi-agent orchestration architecture]

## 🚀 Features

[Core capabilities breakdown]

## 🔌 Plugins

[8 business group plugins]

## 🤖 Agents

[84+ specialized agents]

## 📚 Documentation

[Navigation to all docs]

## 🛠️ Installation & Setup

[Getting started guide]

## 📊 Statistics

[Project metrics]

## 🤝 Contributing

[Contribution guidelines]

## 📄 License

[License information]
```

### Type 2: Plugin Root README

**Location**: `/plugins/[组名]/README.md`

**Purpose**: Entry point for specific business group plugin

**Structure**:
```markdown
# [组名] Plugin

> [Professional tagline]

[![Agents](https://img.shields.io/badge/agents-XX-blue)]()
[![Commands](https://img.shields.io/badge/commands-XX-green)]()
[![Skills](https://img.shields.io/badge/skills-XX-orange)]()

## 📋 Overview

[Plugin description and positioning]

## 🤖 Agent Architecture

[Agent organization and hierarchy]

## 🛠️ Commands & Skills

[Available commands and skills]

## 🚀 Usage Guide

[How to use this plugin]

## 📁 Project Structure

[Directory tree]

## 🎯 Best Practices

[Guidelines and recommendations]

## 📚 Documentation

[Links to subdirectory READMEs]
```

---

## Change Detection Logic

### Git Diff Analysis

```bash
# Detect changes using git diff
git diff --name-status HEAD~10..HEAD

# Analyze output to identify:
# - New plugins (A plugins/新组/)
# - Deleted plugins (D plugins/旧组/)
# - Agent changes (M plugins/*/agents/*.md)
# - Command changes (M .claude/commands/*.md)
# - Skill changes (M .claude/skills/*/)
# - Structure changes (plugin.json, CLAUDE.md)
```

### Python Implementation

```python
import subprocess
from pathlib import Path

def detect_changes_via_git():
    """Detect project changes using git diff"""

    # Run git diff to get changes since HEAD~10
    result = subprocess.run(
        ['git', 'diff', '--name-status', 'HEAD~10..HEAD'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Fallback: analyze current state without delta
        return analyze_current_state()

    # Parse git diff output
    recent_changes = {
        'plugins_changed': [],
        'agents_added': [],
        'agents_removed': [],
        'commands_changed': [],
        'skills_changed': [],
        'structure_changed': False
    }

    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        parts = line.split('\t', 1)
        if len(parts) < 2:
            continue

        status, filepath = parts[0], parts[1]

        # Parse plugins changes
        if 'plugins/' in filepath:
            plugin_match = re.search(r'plugins/([^/]+)', filepath)
            if plugin_match:
                plugin_name = plugin_match.group(1)
                if plugin_name not in recent_changes['plugins_changed']:
                    recent_changes['plugins_changed'].append(plugin_name)

        # Parse agent changes
        if 'agents/' in filepath and filepath.endswith('.md'):
            if status == 'A':
                recent_changes['agents_added'].append(Path(filepath).name)
            elif status == 'D':
                recent_changes['agents_removed'].append(Path(filepath).name)

        # Parse other changes
        if 'commands/' in filepath:
            recent_changes['commands_changed'].append(Path(filepath).name)

        if 'skills/' in filepath:
            recent_changes['skills_changed'].append(Path(filepath).name)

        if filepath in ['plugin.json', 'CLAUDE.md', '.claude/settings.json']:
            recent_changes['structure_changed'] = True

    return recent_changes

def analyze_current_state():
    """Fallback: analyze current project state without git history"""
    # Scan entire project structure
    # Return comprehensive analysis
    pass
```

---

## Comprehensive Project Analysis

### Plugin Discovery

```python
def discover_all_plugins(plugins_dir='plugins'):
    """Discover all plugins and their metadata"""

    plugins = []

    for plugin_dir in Path(plugins_dir).iterdir():
        if not plugin_dir.is_dir() or plugin_dir.name.startswith('.'):
            continue

        plugin_json = plugin_dir / '.claude-plugin' / 'plugin.json'
        if not plugin_json.exists():
            plugin_json = plugin_dir / 'plugin.json'

        metadata = {
            'name': plugin_dir.name,
            'agents': count_agents(plugin_dir / 'agents'),
            'commands': count_commands(plugin_dir / 'commands'),
            'skills': count_skills(plugin_dir / 'skills'),
            'has_readme': (plugin_dir / 'README.md').exists()
        }

        if plugin_json.exists():
            import json
            with open(plugin_json, 'r', encoding='utf-8') as f:
                plugin_meta = json.load(f)
                metadata['description'] = plugin_meta.get('description', '')
                metadata['version'] = plugin_meta.get('version', '1.0.0')

        plugins.append(metadata)

    return plugins
```

### Global Statistics

```python
def calculate_global_statistics(plugins):
    """Calculate project-wide statistics"""

    stats = {
        'total_plugins': len(plugins),
        'total_agents': sum(p['agents'] for p in plugins),
        'total_commands': sum(p['commands'] for p in plugins),
        'total_skills': sum(p['skills'] for p in plugins),
        'plugins_with_agents': len([p for p in plugins if p['agents'] > 0]),
        'plugins_with_commands': len([p for p in plugins if p['commands'] > 0]),
        'plugins_with_skills': len([p for p in plugins if p['skills'] > 0]),
        'largest_plugin': max(plugins, key=lambda p: p['agents'])['name'],
        'documentation_coverage': len([p for p in plugins if p['has_readme']]) / len(plugins) * 100
    }

    return stats
```

---

## Professional README Generation

### Project Root Template

```markdown
# {project_name}

> {tagline}

[![Agents](https://img.shields.io/badge/agents-{total_agents}+-blue)](plugins/)
[![Plugins](https://img.shields.io/badge/plugins-{total_plugins}-green)](plugins/)
[![Skills](https://img.shields.io/badge/skills-{total_skills}+-orange)](.claude/skills/)
[![Status](https://img.shields.io/badge/status-{status}-brightgreen)]()
[![Claude Code](https://img.shields.io/badge/Claude_Code-v{version}-purple)]()

## 📋 Project Overview

{comprehensive_description}

**Core Value Proposition**:
- {value_prop_1}
- {value_prop_2}
- {value_prop_3}

## 🏗️ Architecture

### Three-Layer Agent Architecture

```
Layer 1: Knowledge Layer (.claude/agents/ + .claude/skills/)
  ├── Agents: Role-based decision frameworks
  └── Skills: Self-contained capability packages

Layer 2: Orchestration Layer (Claude Reasoning)
  ├── Dynamic capability composition
  └── Intelligent task routing

Layer 3: Execution Layer (Tools + Output)
  ├── Tool execution (Bash, Python, API, MCP)
  └── Results → output/[项目名]/[agent-name]/
```

### Multi-Agent Orchestration

{architecture_diagram_or_description}

## 🚀 Core Features

{feature_breakdown_by_plugin}

## 🔌 Business Group Plugins

{plugins_table_with_stats}

## 🤖 Agent Overview

**Total: {total_agents} Specialized Agents**

{agent_breakdown_by_plugin}

## 📚 Documentation

### Main Documentation
- [Project Instructions](CLAUDE.md) - Claude Code configuration
- [Architecture Guide](docs/architecture.md)
- [Development Guide](docs/development.md)

### Plugin Documentation
{links_to_all_plugin_readmes}

### Subdirectory Documentation
- [Commands](commands/README.md)
- [Skills](skills/README.md)
- [Agents](agents/README.md)

## 🛠️ Installation & Setup

{installation_guide}

## 🎯 Quick Start

{quick_start_examples}

## 📊 Project Statistics

{detailed_statistics_table}

## 🤝 Contributing

{contribution_guidelines}

## 📄 License

{license_information}

## 🔗 Related Resources

{external_links_and_references}

---

**Version**: {version}
**Last Updated**: {date}
**Maintained by**: {maintainer}
**Status**: ✅ {status}
```

### Plugin Root Template

Similar structure but focused on single plugin scope. (See subdirectory-readme-sync for examples)

---

## Smart Update Strategies

### Strategy 1: Full Regeneration

**When**: Major structural changes, new plugins, significant refactoring

**Process**:
1. Scan entire project fresh
2. Generate complete new README
3. Preserve only user-marked manual sections (`<!-- MANUAL -->`)
4. Full validation

### Strategy 2: Incremental Update

**When**: Minor changes, agent additions, small tweaks

**Process**:
1. Identify changed sections (via git diff)
2. Update only affected sections:
   - Plugin count badges
   - Agent statistics
   - Feature lists
3. Leave rest unchanged
4. Partial validation (only updated sections)

### Strategy 3: Metadata-Only Update

**When**: Version bumps, status changes, date updates

**Process**:
1. Update only metadata section:
   - Version number
   - Last updated date
   - Status badges
2. No structural changes
3. Quick validation

---

## Quality Validation

### Comprehensive Checklist

```python
def validate_root_readme(readme_path, project_scope='root'):
    """Validate root README completeness and quality"""

    content = Path(readme_path).read_text(encoding='utf-8')

    checks = {
        # Structural completeness
        'has_title': content.startswith('# '),
        'has_tagline': '>' in content[:200],
        'has_badges': '![' in content[:500] or 'badge' in content[:500],
        'has_overview': '## 📋' in content or '## Overview' in content,
        'has_architecture': '## 🏗️' in content or '## Architecture' in content,
        'has_features': '## 🚀' in content or '## Features' in content,
        'has_documentation': '## 📚' in content or '## Documentation' in content,
        'has_metadata': '**Version**' in content or '**Last Updated**' in content,

        # Content accuracy
        'plugin_count_accurate': verify_plugin_count(content),
        'agent_count_accurate': verify_agent_count(content),
        'all_plugins_linked': verify_all_plugins_have_links(content),

        # Link validity
        'internal_links_valid': validate_internal_links(content),
        'no_broken_references': check_broken_references(content),

        # Format quality
        'valid_markdown': validate_markdown_syntax(content),
        'proper_heading_hierarchy': check_heading_levels(content),
        'no_trailing_whitespace': not content.endswith(' \n'),

        # Professional standards
        'has_professional_tone': True,  # Manual review recommended
        'badges_properly_formatted': verify_badge_format(content),
        'tables_well_formatted': verify_table_format(content)
    }

    return all(checks.values()), checks
```

---

## Template Customization

### Customization Points

Users can customize via config file `.claude/skills/齐头并进/root-readme-sync/config.yaml`:

```yaml
project_name: "ZTL数智化作战中心"
tagline: "AI-Powered Multi-Agent Orchestration Platform"

badges:
  include: true
  style: "flat-square"  # or "flat", "plastic", "for-the-badge"
  custom_badges:
    - label: "Version"
      message: "1.0.0"
      color: "blue"

sections:
  include_architecture: true
  include_features: true
  include_quick_start: true
  include_statistics: true
  include_contributing: true

format:
  emoji_style: true  # Use emojis in headers
  table_of_contents: true
  collapsible_sections: false

links:
  include_external: true
  github_repo: "https://github.com/ZTL-Digital/ops-center"

metadata:
  author: "ZTL Digital Intelligence Operations Center"
  license: "MIT"
  maintained_by: "Development Team"
```

---

## Error Handling

### Common Issues

**Issue 1**: Git diff unavailable or repo not initialized
- **Solution**: Fallback to full project scan (analyze current state)
- **Log**: Warning logged to .claude/logs/skill-errors.log
- **Recovery**: Generate from current state (no delta detection)

**Issue 2**: Plugin metadata missing (no plugin.json)
- **Solution**: Use directory name and scan results as fallback
- **Impact**: Description may be generic
- **Notification**: Warn user about missing metadata

**Issue 3**: Existing README has major manual customizations
- **Solution**: Detect manual sections (marked with `<!-- MANUAL START -->` and `<!-- MANUAL END -->`), preserve them
- **Process**: Insert updated sections around preserved manual content
- **Validation**: Ensure no content loss

**Issue 4**: Link validation failures
- **Solution**: Log broken links, continue generation
- **Output**: Include "⚠️ Warning: X broken links detected" in summary
- **Action**: Recommend manual review

---

## Integration

### With subdirectory-readme-sync

Typical workflow:
```
1. User makes changes to agents/
2. subdirectory-readme-sync updates agents/README.md
3. root-readme-sync detects subdirectory README updated
4. root-readme-sync updates root README with new agent count
```

### With /readme-generator command

The `/readme-generator` command orchestrates both skills:
```bash
/readme-generator

# Internally:
1. Run subdirectory-readme-sync for all subdirectories
2. Run root-readme-sync for root and all plugin roots
3. Validate all generated READMEs
4. Generate comprehensive report
```

---

## Performance Optimization

### Caching Strategy

```python
# Cache plugin metadata to avoid re-scanning
cache = {
    'plugins': {},
    'last_scan': None,
    'ttl': 300  # 5 minutes
}

def get_plugins_cached():
    if cache['last_scan'] and (time.time() - cache['last_scan'] < cache['ttl']):
        return cache['plugins']

    cache['plugins'] = discover_all_plugins()
    cache['last_scan'] = time.time()
    return cache['plugins']
```

### Incremental Processing

- Only re-analyze plugins that changed (from git diff)
- Reuse existing statistics for unchanged plugins
- Update only affected README sections

**Performance gains**:
- Full scan: ~2-3 seconds
- Incremental: ~300-500ms

---

## Examples

### Example 1: Full project README update

```
User: "更新项目主README,结构改了很多"

Skill workflow:
1. Git diff → Detect 3 new plugins, 10 new agents
2. Full project scan:
   - 8 plugins (was 5)
   - 84 agents (was 74)
   - 15 skills (was 12)
3. Generate complete new README:
   - Update badges: agents-74+ → agents-84+
   - Add 3 new plugins to table
   - Regenerate statistics section
   - Update architecture description
4. Validate: ✅ All plugins documented, all links valid
5. Write /README.md
6. Report: "✅ Updated README.md (8 plugins, 84 agents, 15 skills)"
```

### Example 2: Plugin root README update

```
User: "开发组agents增加了,更新plugins/开发组/README.md"

Skill workflow:
1. Git diff → Detect 2 agents added to 开发组
2. Scan plugins/开发组/:
   - 19 agents (was 17)
   - 6 commands
   - 1 skill
3. Read existing README
4. Incremental update:
   - Badges: agents-17 → agents-19
   - Agent list: add F17, F18
   - Architecture section: update count
5. Validate: ✅ All 19 agents documented
6. Write plugins/开发组/README.md
7. Report: "✅ Updated 开发组/README.md (19 agents)"
```

---

## Best Practices

1. **Run after major milestones** - Sprint end, version release, major refactoring
2. **Ensure git is up-to-date** - Commit recent changes before running for accurate diff detection
3. **Review before committing** - Generated content should be verified
4. **Preserve manual customizations** - Use `<!-- MANUAL -->` markers
5. **Validate thoroughly** - Run full validation checklist
6. **Update incrementally when possible** - Faster and less risky
7. **Keep templates updated** - As project evolves, update templates

---

## Maintenance

### When to Update This Skill

- New plugin structure/organization emerges
- README template standards change
- GitHub badge APIs update
- New sections needed (e.g., Security, Roadmap)
- Validation rules change

---

## 🚀 执行指令 (Execution Instructions)

**⚠️ 重要**: 当Claude需要更新root README时,请严格按照以下步骤执行。

### Step 1: 运行统计分析引擎

**Claude,请执行以下命令获取实时准确的项目统计数据**:

```bash
python3 .claude/skills/齐头并进/root-readme-sync/scripts/readme_analyzer.py
```

**预期输出**: JSON格式的完整项目统计
```json
{
  "agents": {
    "business_agents": 84,
    "system_agents": 9,
    "total_agents": 93,
    "by_group": {
      "战略组": 9,
      "创意组": 16,
      "情报组": 8,
      ...
    }
  },
  "commands": {
    "total": 13,
    "commands": ["prp", "test", "context-aware", ...]
  },
  "skills": {
    "total": 22,
    "skills": [...]
  },
  "mcp_servers": {
    "total": 7,
    "servers": ["chrome-mcp", "github-mcp", ...]
  },
  "plugins": {...},
  "timestamp": "2025-11-01T...",
  "version": "1.1.0"
}
```

### Step 2: 使用统计数据更新README

**Claude,请使用Step 1获取的准确数据,更新README.md的以下部分**:

1. **项目概述部分** (第8行附近):
   - 更新智能体总数: `协调 **{total_agents}个专业智能体**`
   - 更新业务组数量: `横跨 **8大业务组**` (固定)

2. **核心特性部分** (第28-30行附近):
   - 更新: `**{total_agents}个专业智能体**: {business_agents}个业务组智能体 + {system_agents}个系统级智能体`
   - 更新: `**{commands.total}个斜杠命令**`
   - 更新: `**{skills.total}个技能包**`

3. **业务组概览表格** (第163-171行附近):
   - 根据`by_group`数据更新每个业务组的智能体数量
   - 格式: `| **战略组** (Strategy) | {by_group['战略组']}个 | 核心职能 |`

4. **命令系统部分** (第179行附近):
   - 更新: `提供 **{commands.total}个斜杠命令** 用于一键式工作流`

5. **项目统计部分** (第205-209行附近):
   - 智能体总数: `**{total_agents}个** ({business_agents}个业务组智能体 + {system_agents}个系统级智能体)`
   - 斜杠命令: `**{commands.total}个**`
   - 技能包: `**{skills.total}个**`
   - MCP服务器: `**{mcp_servers.total}+个**`

### Step 3: 运行准确性验证

**Claude,请执行验证脚本确保更新后的README准确无误**:

```bash
python3 .claude/skills/齐头并进/root-readme-sync/scripts/validator.py README.md .
```

**预期输出**:
```
📊 README准确性验证报告
======================================================================

✅ 验证通过的项目 (8个):
✅ 智能体总数准确: 93个
✅ 命令数量准确: 13个
✅ 技能包数量准确: 22个
✅ 业务组表格数据准确
✅ 所有内部链接有效
✅ Markdown语法检查完成

======================================================================
✨ 完美! README信息准确无误,所有检查通过。
======================================================================
```

**如果验证失败**:
- ❌ 查看错误报告,识别不准确的部分
- 🔧 重新执行Step 1获取最新数据
- 🔄 返回Step 2,使用准确数据修正
- ✅ 重新运行Step 3验证,直到通过

### Step 4: 更新元数据

**Claude,请更新README底部的元数据**:

```markdown
**文档生成**: 自动更新于 {当前日期} by `/github-pull` 命令
**版本**: v{project_version}
**最后更新**: {当前日期}
**更新内容**: {简要描述本次更新的内容}
```

---

## 工作流集成

### 在github-pull命令中的调用方式

在`.claude/commands/github-pull.md`的Step 0.5中:

```markdown
**0.5 调用 root-readme-sync 技能包**

**Claude,请现在执行以下操作**:

1. **运行统计引擎**:
   ```bash
   python3 .claude/skills/齐头并进/root-readme-sync/scripts/readme_analyzer.py
   ```

2. **解析输出的JSON数据** (会保存到 `output/project-stats.json`)

3. **使用统计数据更新README.md**:
   - 按照root-readme-sync skill的Step 2指令执行
   - 确保所有统计数据使用实时扫描的准确值

4. **运行验证**:
   ```bash
   python3 .claude/skills/齐头并进/root-readme-sync/scripts/validator.py
   ```

5. **如果验证失败,中止github-pull流程并报告错误**
```

---

## 故障排查

### 常见问题

**Q1: 统计脚本报错 "ModuleNotFoundError: No module named 'yaml'"**
- **解决方案**: 安装依赖 `pip install pyyaml`

**Q2: 验证失败,提示数量不匹配**
- **原因**: README可能包含手动编辑的内容
- **解决方案**: 重新运行统计脚本,使用最新数据覆盖

**Q3: JSON输出格式错误**
- **解决方案**: 检查Python版本 ≥3.8,确保编码为UTF-8

---

## Related Documentation

- [subdirectory-readme-sync SKILL.md](../subdirectory-readme-sync/SKILL.md) - Subdirectory README sync
- [/readme-generator command](../../../commands/readme-generator.md) - Full README generator command
- [Global CLAUDE.md](~/.claude/CLAUDE.md) - Project configuration standards
- [readme_analyzer.py](./scripts/readme_analyzer.py) - 统计分析引擎源码
- [validator.py](./scripts/validator.py) - 验证器源码

---

**Skill Version**: 2.0.0
**Created**: 2025-11-01
**Last Updated**: 2025-11-01
**Status**: ✅ Production Ready (新增执行引擎层)
**Maintained by**: ZTL Digital Intelligence Operations Center
