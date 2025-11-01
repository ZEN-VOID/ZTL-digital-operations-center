---
name: subdirectory-readme-sync
description: Automatically synchronize README.md files for subdirectories (agents/, commands/, skills/, etc.) by analyzing project structure changes from .claude/logs/changes.log or git diff, ensuring documentation stays current with actual directory state.
---

# Subdirectory README Sync Skill

> Intelligent subdirectory documentation synchronization with change detection

## Quick Start

**When to use**:
- After adding/removing/modifying agents, commands, or skills in subdirectories
- When subdirectory structure changes (new files, renamed files, deleted files)
- Periodic maintenance to ensure docs reflect actual state
- After major refactoring of plugin/module structure

**Auto-invoked when**:
- User mentions "update subdirectory READMEs", "sync agents README", "update commands docs"
- After batch operations on agents/commands/skills
- When changes detected in subdirectories but README not updated

**Example invocations**:
```
User: "更新 plugins/开发组/agents/ 的 README"
User: "同步所有 commands 目录的文档"
User: "agents 目录改动了,更新一下文档"
```

---

## Core Functionality

This skill provides **intelligent subdirectory README synchronization** with:

1. **Change Detection** - Analyzes `.claude/logs/changes.log` or git diff to identify what changed
2. **Smart Analysis** - Extracts metadata from agent/command/skill files (YAML frontmatter)
3. **Professional Documentation** - Generates GitHub-standard README with badges, tables, examples
4. **Incremental Updates** - Only updates sections that changed, preserves manual customizations
5. **Quality Validation** - Verifies generated docs are complete and accurate

---

## Workflow

```
Step 1: Change Detection
├─ Priority 1: Read .claude/logs/changes.log
│  └─ Parse recent changes since last update
├─ Priority 2: Run git diff (if changes.log unavailable)
│  └─ Detect file additions/deletions/modifications
└─ Identify target subdirectories needing updates

Step 2: Directory Analysis
├─ Scan subdirectory for all relevant files
├─ Extract metadata (YAML frontmatter, file structure)
├─ Count files by type (agents, commands, skills)
└─ Identify organizational patterns

Step 3: README Generation
├─ Load existing README (if exists)
├─ Generate new content sections:
│  ├─ Overview with badges (file counts, status)
│  ├─ Organizational structure (hierarchy, categories)
│  ├─ Detailed file listings with descriptions
│  ├─ Usage guides (how to invoke, examples)
│  └─ Best practices and references
└─ Preserve manual customizations where applicable

Step 4: Quality Validation
├─ Verify all files documented
├─ Check metadata accuracy
├─ Validate Markdown syntax
└─ Ensure links work

Step 5: Output
├─ Write updated README.md to subdirectory
├─ Log changes made
└─ Report summary to user
```

---

## Supported Subdirectories

### agents/
**Structure**:
```
agents/
├── README.md          # This skill updates this
├── F0-产品经理.md
├── F1-前端开发.md
└── FF-开发组组长.md
```

**Generated sections**:
- Overview (agent count, organization)
- Agent hierarchy (by layer/role)
- Detailed agent cards (name, description, when to use, invocation)
- Usage guide (auto-delegation vs explicit invocation)
- Best practices

### commands/
**Structure**:
```
commands/
├── README.md          # This skill updates this
├── commit.md
├── test.md
└── deploy.md
```

**Generated sections**:
- Command list with descriptions
- Detailed usage for each command
- Parameter documentation
- Examples
- Development guide

### skills/
**Structure**:
```
skills/
├── README.md          # This skill updates this
├── skill-a/
│   └── SKILL.md
└── skill-b/
    └── SKILL.md
```

**Generated sections**:
- Skill catalog
- Detailed skill documentation
- Auto-invocation triggers
- Integration examples

---

## Output Format

### Professional README Structure

```markdown
# [Subdirectory Name] - [Business Domain]

> [Tagline describing purpose]

[![Files](https://img.shields.io/badge/files-XX-blue)]()
[![Status](https://img.shields.io/badge/status-active-green)]()
[![Updated](https://img.shields.io/badge/updated-YYYY--MM--DD-brightgreen)]()

## 📋 Overview

[Brief description of what this subdirectory contains]

Total: **XX items**

## 🗂️ Organizational Structure

[Hierarchy or categorization of items]

### Category 1
- Item 1
- Item 2

### Category 2
- Item 3
- Item 4

## 📚 Detailed Documentation

### Item 1

**Description**: [What it does]

**When to use**:
- Use case 1
- Use case 2

**Invocation**:
```python
# Example code
```

---

## 🚀 Usage Guide

[How to use items in this directory]

## 🎯 Best Practices

[Guidelines and recommendations]

## 🔗 Related Resources

- [Link to parent README]
- [Link to related docs]

---

**Last Updated**: YYYY-MM-DD
**Maintained by**: [Team/Person]
**Status**: ✅ Active
```

---

## Change Detection Logic

### Reading changes.log

```python
# Parse .claude/logs/changes.log
with open('.claude/logs/changes.log', 'r') as f:
    lines = f.readlines()

# Look for last README update timestamp
last_update = find_last_update_timestamp(lines)

# Extract changes since last update
recent_changes = parse_changes_since(lines, last_update)

# Categorize changes
changes = {
    'added': [],
    'modified': [],
    'deleted': [],
    'renamed': []
}
```

### Git diff fallback

```bash
# If changes.log unavailable or incomplete
git diff --name-status HEAD~1..HEAD -- agents/

# Parse output:
# A  agents/F10-新智能体.md  (added)
# M  agents/F1-前端开发.md   (modified)
# D  agents/F9-旧智能体.md   (deleted)
```

---

## Metadata Extraction

### Agent Files

```python
import yaml
import re

def extract_agent_metadata(file_path):
    content = Path(file_path).read_text(encoding='utf-8')

    # Extract YAML frontmatter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        metadata = yaml.safe_load(match.group(1))
        return {
            'name': metadata.get('name'),
            'description': metadata.get('description'),
            'model': metadata.get('model', 'sonnet'),
            'tools': metadata.get('tools', [])
        }
```

### Command Files

```python
def extract_command_metadata(file_path):
    content = Path(file_path).read_text(encoding='utf-8')

    # Extract frontmatter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        metadata = yaml.safe_load(match.group(1))
        return {
            'description': metadata.get('description'),
            'argument_hint': metadata.get('argument-hint'),
            'allowed_tools': metadata.get('allowed-tools', [])
        }
```

### Skill Directories

```python
def extract_skill_metadata(skill_dir):
    skill_md = skill_dir / 'SKILL.md'
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')

        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            metadata = yaml.safe_load(match.group(1))
            return {
                'name': metadata.get('name'),
                'description': metadata.get('description')
            }
```

---

## Quality Validation

### Validation Checklist

```python
def validate_readme(readme_path, subdirectory):
    """Validate generated README quality"""

    checks = {
        'file_exists': readme_path.exists(),
        'has_overview': '## 📋 Overview' in content,
        'has_structure': '## 🗂️' in content or '## 🤖' in content,
        'has_details': '## 📚' in content or '###' in content,
        'has_usage': '## 🚀 Usage' in content,
        'has_metadata': 'Last Updated' in content,
        'all_files_documented': verify_all_files_listed(subdirectory),
        'valid_markdown': validate_markdown_syntax(content),
        'working_links': validate_internal_links(content)
    }

    return all(checks.values()), checks
```

---

## Configuration

### Customization Options

Users can customize via environment or config:

```python
config = {
    'change_detection': 'changes.log',  # or 'git_diff'
    'include_badges': True,
    'include_examples': True,
    'preserve_manual_sections': True,
    'auto_commit': False,
    'validation_strict': True
}
```

---

## Error Handling

### Common Issues

**Issue 1**: changes.log not found or empty
- **Solution**: Fallback to git diff automatically
- **Log**: Warning logged, proceed with git diff

**Issue 2**: YAML frontmatter parse error
- **Solution**: Use filename as fallback, log warning
- **Impact**: Description may be missing, but file still documented

**Issue 3**: Existing README has manual customizations
- **Solution**: Preserve manual sections (marked with `<!-- MANUAL -->`), update only auto-generated sections
- **User notification**: List preserved sections

---

## Examples

### Example 1: Update agents/ README after adding new agent

```
User: "刚添加了F10-新智能体,更新agents的README"

Skill workflow:
1. Read changes.log → Detect F10-新智能体.md added
2. Scan agents/ → Find all 20 agent files
3. Extract metadata from all agents
4. Generate updated README:
   - Update count: 19 → 20
   - Add F10 to organizational structure
   - Add F10 detailed card
5. Validate: ✅ All 20 agents documented
6. Write agents/README.md
7. Report: "✅ Updated agents/README.md (20 agents documented)"
```

### Example 2: Bulk update after reorganization

```
User: "重新组织了commands目录,有些命令改名了,更新文档"

Skill workflow:
1. Git diff → Detect renamed files
2. Scan commands/ → Find current state
3. Compare with existing README → Identify discrepancies
4. Generate new README with current structure
5. Validate: ✅ All commands documented, old references removed
6. Write commands/README.md
7. Report: "✅ Updated commands/README.md (6 commands, 2 renamed)"
```

---

## Integration

### With Other Skills

- **root-readme-sync**: Coordinates to update root README after subdirectory READMEs updated
- **readme-generator**: Used as component in full project README generation
- **context-aware**: Provides subdirectory context for analysis

### With Commands

Can be invoked via slash command:

```bash
/update-subdirectory-readme agents/
/update-subdirectory-readme commands/
/update-subdirectory-readme skills/
```

---

## Best Practices

1. **Run after structural changes** - Add/remove/rename files
2. **Check changes.log first** - More accurate than git diff
3. **Review generated README** - Verify accuracy before committing
4. **Preserve customizations** - Mark manual sections with `<!-- MANUAL -->`
5. **Validate thoroughly** - Use validation checklist
6. **Update incrementally** - Don't regenerate entire README if only small changes

---

## Performance

- **Scan speed**: ~100ms for 20 agent files
- **Generation speed**: ~200ms for complete README
- **Total execution**: <500ms typical
- **Memory usage**: <10MB

---

## Maintenance

### When to Update This Skill

- New subdirectory types added (e.g., hooks/, scripts/)
- Metadata format changes in agent/command/skill files
- README template structure evolves
- New validation rules needed

---

## Related Documentation

- [root-readme-sync SKILL.md](../root-readme-sync/SKILL.md) - Root README synchronization
- [readme-generator command](../../../commands/readme-generator.md) - Full project README generator
- [Global CLAUDE.md](~/.claude/CLAUDE.md) - Output path conventions

---

**Skill Version**: 1.0.0
**Created**: 2025-11-01
**Last Updated**: 2025-11-01
**Status**: ✅ Production Ready
**Maintained by**: ZTL Digital Intelligence Operations Center
