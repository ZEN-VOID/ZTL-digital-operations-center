# MANUS Command Restructuring Design Document

> **Version**: v1.0.0
> **Date**: 2025-10-23
> **Author**: Claude (Sonnet 4.5)
> **Status**: Design Phase

---

## 📋 Executive Summary

This document specifies the complete restructuring of context management commands (C/X/Z) into a unified MANUS command, implementing production-grade context engineering principles while transitioning from a three-tier to dual-tier configuration system.

**Key Changes**:
- ✅ Merge three commands (C/X/Z) into single MANUS command
- ✅ Transition from three-tier (machine/system/project) to **dual-tier (global/project)**
- ✅ Integrate MANUS context engineering best practices (KV-cache optimization, error preservation, file-based context)
- ✅ Consolidate 9 content sections into unified structure
- ✅ Maintain organic growth memory with append-only updates

---

## 1. Context Engineering Principles

### 1.1 MANUS Core Principles

Based on production AI agent systems, MANUS implements:

```yaml
KV-Cache Optimization:
  Cost Impact: Cached tokens $0.30/MTok vs uncached $3.00/MTok (10x difference)
  Principle: Stable prefixes maximize cache reuse
  Implementation: Append-only context, never modify previous entries
  Cache Breakpoints: Manual management accounting for expiration patterns

Attention Management:
  Problem: "Lost in the middle" - models struggle with mid-context information
  Solution: Task recitation through structured todo files
  Implementation: Enhanced TODO section with explicit attention anchors

Error Preservation:
  Philosophy: "Error recovery is clearest indicator of true agentic behavior"
  Principle: Failed actions and stack traces provide crucial learning signals
  Implementation: Complete ERROR/RECOVERY/ADAPTATION sections

File System-Based Context:
  Advantage: Unlimited persistent external memory
  Principle: File system as recoverable compression storage
  Implementation: Drop verbose content but preserve restoration paths (URLs, file paths)

Organic Growth Memory:
  Structure: Timestamp-based append-only updates
  Philosophy: Preserve complete evolution history
  Implementation: Never delete, always append with timestamps
```

### 1.2 Why Three-Tier to Dual-Tier?

**Problem with Three-Tier System**:
```yaml
Original Classification:
  Machine Level: ~/.claude/CLAUDE.md (cross all frameworks and projects)
  System Level: .claude/CLAUDE.md (framework-specific, cross-project)
  Project Level: CLAUDE.md (project-specific)

Issues:
  ❌ Confusion: "System" vs "Machine" distinction unclear to users
  ❌ Overhead: Three-tier decision tree adds cognitive load
  ❌ Cache Breaking: Multi-level classification variations break KV-cache
  ❌ Maintenance: Three files to manage context across
```

**Dual-Tier Solution**:
```yaml
New Classification:
  Global Level: ~/.claude/CLAUDE.md (machine + system merged)
    - Cross all projects and frameworks
    - Personal/team-wide knowledge base
    - Reusable patterns and solutions

  Project Level: CLAUDE.md (unchanged)
    - Project-specific context
    - Local decisions and errors
    - Project-scoped learning

Benefits:
  ✅ Clarity: Clear distinction between global vs project
  ✅ Simplicity: Two-tier decision is faster and more deterministic
  ✅ Cache Efficiency: Reduced classification variations
  ✅ Maintenance: Only two files to manage
```

---

## 2. Unified MANUS Structure

### 2.1 Content Section Consolidation

**Original 9 Sections Across C/X/Z**:

```yaml
From C.md (Attention Control):
  - 🎯 FOCUS (Current Attention Focus)
  - 📋 TODO (Tasks and Action Plans)
  - ⚙️ PROCESS (Process Records)

From X.md (Error Correction):
  - ❌ ERROR (Error Recording)
  - 🔧 RECOVERY (Error Recovery)
  - 🔄 ADAPTATION (Adaptive Adjustments)
  - 📈 IMPROVEMENT (Continuous Improvement)
  - 🔍 PATTERNS (Error Patterns) ← Duplicate with Z

From Z.md (Knowledge Accumulation):
  - 💡 EXPERIENCES (Technical Experiences)
  - 🧠 INSIGHTS (Technical Insights)
  - 🔍 PATTERNS (Technical Patterns) ← Duplicate with X
  - 🚀 SOLUTIONS (Innovative Solutions)
  - 🛠️ TECHNIQUES (Practical Techniques)
```

**Consolidated 7 Sections for MANUS**:

```yaml
Active Context (Real-time):
  1. 🎯 FOCUS - Current attention and priorities
  2. 📋 TODO - Task recitation for attention management
  3. ⚙️ PROCESS - Active process execution records

Learning Context (Historical):
  4. ❌ ERROR - Error preservation with full context
  5. ✅ SUCCESS - Successful experiences and solutions (merged EXPERIENCES + SOLUTIONS)
  6. 🧠 INSIGHTS - Deep technical insights (merged INSIGHTS + TECHNIQUES)
  7. 🔍 PATTERNS - Consolidated patterns (merged both PATTERNS sections)

Rationale:
  - Merge duplicate PATTERNS sections
  - Combine positive learning (EXPERIENCES + SOLUTIONS → SUCCESS)
  - Merge deep knowledge (INSIGHTS + TECHNIQUES → INSIGHTS)
  - Remove RECOVERY/ADAPTATION/IMPROVEMENT as subsections of ERROR
```

### 2.2 Section Structure Details

#### Section 1: 🎯 FOCUS (Current Attention Focus)

```markdown
## 🎯 FOCUS

### Active Attention Anchors

#### 🕐 2025-10-23T14:30:00 🎯 Current Focus: [Description]
- 📊 Priority: HIGH/MEDIUM/LOW
- ⏱️ Expected Duration: [Time estimate]
- 🎯 Success Criteria: [Specific measurable criteria]
- 🔗 Related Context: [Links to relevant sections/files]
- 💭 Rationale: [Why this is current focus]

**Cache Optimization Note**: Focus entries use stable timestamp prefixes to maximize KV-cache reuse.
```

**Design Principles**:
- Stable prefix: `🕐 [Timestamp] 🎯`
- Explicit success criteria for attention management
- Links to related context for cache locality
- One active focus at a time (append new when switching)

---

#### Section 2: 📋 TODO (Task Recitation)

```markdown
## 📋 TODO

### Task List (Attention Management)

#### 🕐 2025-10-23T14:30:00 ⭕ Task: [Description]
- 🏷️ Type: DEV/DOC/CONFIG/TEST/REVIEW/DEPLOY/RESEARCH
- 📊 Priority: HIGH/MEDIUM/LOW
- 🎯 Completion Criteria: [Specific criteria]
- 🔗 Dependencies: [Task IDs or file paths]
- 📝 Notes: [Additional context]
- **Status**: ⭕Pending → 🔄InProgress → ✅Done / ❌Cancelled / 🚫Blocked / ⏸️Paused

**Task Recitation Principle**: Explicit task lists combat "lost in the middle" problem by providing attention anchors.
```

**Design Principles**:
- Status transitions preserve complete history (append-only)
- Explicit dependencies for context graph
- Task recitation as attention management tool
- Links to file paths enable recoverable compression

---

#### Section 3: ⚙️ PROCESS (Process Execution Records)

```markdown
## ⚙️ PROCESS

### Process Execution History

#### 🕐 2025-10-23T14:30:00 ⚙️ Process: [Name]
- 🏷️ Type: DEVELOP/DEBUG/OPTIMIZE/LEARN/REVIEW/REFACTOR
- 📝 Key Steps: [Step1] → [Step2] → [Step3]
- ⏱️ Duration: [Actual time]
- 💡 Learnings: [Key takeaways]
- 🔗 Related Files: [File paths for context recovery]
- 📊 Outcome: SUCCESS/PARTIAL/FAILED

**Cache Optimization**: Process records provide stable context for similar future tasks.
```

**Design Principles**:
- Append-only execution history
- File paths enable recoverable compression
- Explicit outcomes for pattern recognition
- Key steps provide reusable workflow templates

---

#### Section 4: ❌ ERROR (Error Preservation)

```markdown
## ❌ ERROR

### Error Context Preservation

#### 🕐 2025-10-23T14:30:00 ❌ Error: [Description]
- 🏷️ Type: CONFIG/LOGIC/SYSTEM/INTEGRATION/USER/PERMISSION
- 📊 Severity: CRITICAL/HIGH/MEDIUM/LOW
- 🎯 Failed Action: [Specific action that failed]
- 📝 Full Context:
  ```
  [Complete error context, stack trace, relevant state]
  ```
- 💡 Learning Value: [Why this error matters]
- 🔗 Related Files: [File paths involved]

##### 🔧 Recovery
- 🏷️ Strategy: ROLLBACK/REPAIR/REBUILD/WORKAROUND
- 📝 Steps: [Detailed recovery steps]
- ⏱️ Recovery Time: [Actual time]

##### 🔄 Adaptation
- 📝 Root Cause: [Deep analysis]
- 🔧 Prevention Measures: [Specific changes]
- 📈 System Updates: [Config/code changes]

**Error Preservation Principle**: "Error recovery is clearest indicator of true agentic behavior" - preserve complete error context for learning.
```

**Design Principles**:
- Complete error context preservation (stack traces, state)
- Structured recovery process documentation
- Root cause analysis for prevention
- Learning value explicit for future reference

---

#### Section 5: ✅ SUCCESS (Successful Experiences & Solutions)

```markdown
## ✅ SUCCESS

### Successful Experiences and Solutions

#### 🕐 2025-10-23T14:30:00 ✅ Success: [Description]
- 🏷️ Type: IMPLEMENTATION/OPTIMIZATION/INTEGRATION/DEBUGGING
- 📊 Value Level: HIGH/MEDIUM/LOW
- 🎯 Problem Solved: [Original problem]
- 📝 Solution Approach:
  ```
  [Detailed solution with code/config examples]
  ```
- 📈 Impact: [Measurable improvement]
- 🔗 Related Files: [Implementation file paths]
- 💡 Reusability: [How to apply to other scenarios]

**Solution Template**: [If applicable, provide reusable template]
```

**Design Principles**:
- Merge positive experiences (EXPERIENCES) and innovative solutions (SOLUTIONS)
- Explicit reusability guidance
- Measurable impact for value assessment
- File paths for context recovery

---

#### Section 6: 🧠 INSIGHTS (Deep Technical Insights)

```markdown
## 🧠 INSIGHTS

### Technical Insights and Techniques

#### 🕐 2025-10-23T14:30:00 🧠 Insight: [Title]
- 📊 Depth Level: SURFACE/MODERATE/DEEP/BREAKTHROUGH
- 🏷️ Domain: [Technical domain]
- 💡 Core Insight:
  ```
  [Detailed explanation of insight]
  ```
- 📚 Theoretical Basis: [Why this works]
- 🛠️ Practical Techniques: [How to apply]
- 📈 Innovation Degree: INCREMENTAL/SIGNIFICANT/BREAKTHROUGH
- 🔗 References: [Documentation, articles, file paths]

**Knowledge Depth Principle**: Combine theoretical insights with practical techniques for complete understanding.
```

**Design Principles**:
- Merge theoretical insights (INSIGHTS) and practical techniques (TECHNIQUES)
- Depth level for filtering by complexity
- Theoretical basis for deep understanding
- Practical application guidance

---

#### Section 7: 🔍 PATTERNS (Consolidated Patterns)

```markdown
## 🔍 PATTERNS

### Recognized Patterns (Error + Technical)

#### 🕐 2025-10-23T14:30:00 🔍 Pattern: [Name]
- 🏷️ Category: ERROR_PATTERN/DESIGN_PATTERN/WORKFLOW_PATTERN
- 📊 Frequency: [How often encountered]
- 📝 Pattern Description:
  ```
  [Detailed pattern description]
  ```
- 🎯 When to Apply: [Trigger conditions]
- ⚠️ Anti-Patterns: [What to avoid]
- 💡 Best Practices: [Recommended approach]
- 🔗 Examples: [File paths to examples]

**Pattern Recognition Principle**: Consolidate both error patterns (from X) and technical patterns (from Z) for comprehensive pattern library.
```

**Design Principles**:
- Merge error patterns (from X.md) and technical patterns (from Z.md)
- Category field distinguishes pattern types
- Frequency tracking for priority
- Anti-patterns prevent common mistakes

---

## 3. Dual-Tier Classification Logic

### 3.1 Classification Decision Tree

```yaml
Classification Decision:
  Input: MANUS entry (FOCUS/TODO/PROCESS/ERROR/SUCCESS/INSIGHTS/PATTERNS)

  Question 1: "Is this specific to current project only?"
    YES → Project Level (CLAUDE.md)
      Examples:
        - Project-specific configuration errors
        - Local development workflow
        - Project business logic insights
        - Current project task list

    NO → Continue to Question 2

  Question 2: "Is this reusable across projects/frameworks?"
    YES → Global Level (~/.claude/CLAUDE.md)
      Examples:
        - General programming patterns
        - Tool usage techniques
        - Cross-project workflows
        - Reusable error solutions

    NO → Uncertain, default to Project Level

Simplification Benefits:
  ✅ Two questions vs three-tier decision tree
  ✅ Clear "project-specific" vs "reusable" distinction
  ✅ Default to project level reduces classification errors
  ✅ Stable classification improves KV-cache efficiency
```

### 3.2 Classification Keywords

```yaml
Global Level Indicators:
  - "跨项目" (cross-project)
  - "通用" (general)
  - "框架" (framework)
  - "最佳实践" (best practice)
  - "可复用" (reusable)
  - "技术洞察" (technical insight)
  - "工具使用" (tool usage)

Project Level Indicators:
  - "本项目" (this project)
  - "当前业务" (current business)
  - "项目配置" (project config)
  - "本地开发" (local development)
  - Project name mentioned
  - Specific file paths in current project
```

### 3.3 Migration from Three-Tier

```yaml
Old Three-Tier → New Dual-Tier Mapping:

Machine Level (~/.claude/CLAUDE.md):
  → Global Level (~/.claude/CLAUDE.md)
  Migration: Keep file location, expand scope

System Level (.claude/CLAUDE.md):
  → Global Level (~/.claude/CLAUDE.md)
  Migration: Move framework-generic content to global
  Note: System-specific content stays in project

Project Level (CLAUDE.md):
  → Project Level (CLAUDE.md)
  Migration: No change, same location and scope

Migration Process:
  1. Review .claude/CLAUDE.md (old system level)
  2. Identify framework-generic content → move to global
  3. Identify framework-specific content → keep in project
  4. Delete .claude/CLAUDE.md after migration
  5. Update all references to remove "system level" concept
```

---

## 4. MANUS Command Specification

### 4.1 Command Metadata

```markdown
---
description: "基于MANUS上下文工程的统一上下文管理系统，整合注意力管理、错误学习和知识沉淀，支持全局/项目双层级识别机制"
allowed-tools: ["Read", "Write", "Edit", "Grep"]
version: "2.0.0"
argument-hint: "[Content Type] [Multi-line Parameters]"
---
```

### 4.2 Command Signature

```bash
/manus [TYPE] [PARAMETERS]

Types:
  focus    - 🎯 记录当前注意力焦点
  todo     - 📋 任务管理和注意力锚点
  process  - ⚙️ 流程执行记录
  error    - ❌ 错误保存和恢复学习
  success  - ✅ 成功经验和解决方案
  insights - 🧠 技术洞察和实践技巧
  patterns - 🔍 模式识别和最佳实践

Parameters: Multi-line structured input (emoji-based templates)
```

### 4.3 Multi-line Parameter Templates

```yaml
Focus Template:
  /manus focus
  📊 Priority: HIGH
  ⏱️ Duration: 2h
  🎯 Success: Feature implemented and tested
  💭 Rationale: Critical for v2.0 release

  Current focus description...

TODO Template:
  /manus todo
  🏷️ Type: DEV
  📊 Priority: HIGH
  🎯 Completion: Tests passing
  🔗 Dependencies: feature-x branch

  Task description...

Error Template:
  /manus error
  🏷️ Type: LOGIC
  📊 Severity: HIGH
  🎯 Failed Action: Data validation
  💡 Learning Value: Type safety patterns

  Error context:
  [Stack trace, error message, state]

  Recovery strategy:
  [Steps taken to fix]

Success Template:
  /manus success
  🏷️ Type: OPTIMIZATION
  📊 Value: HIGH
  🎯 Problem: Slow API response
  📈 Impact: 10x faster
  💡 Reusability: Cache pattern applicable to all APIs

  Solution details...

Insights Template:
  /manus insights
  📊 Depth: DEEP
  🏷️ Domain: Caching
  💡 Innovation: SIGNIFICANT

  Core insight:
  [Theoretical explanation]

  Practical techniques:
  [How to apply]

Patterns Template:
  /manus patterns
  🏷️ Category: DESIGN_PATTERN
  📊 Frequency: Common

  Pattern description:
  [When/how to use]

  Anti-patterns:
  [What to avoid]
```

---

## 5. Implementation Specification

### 5.1 File Operations

```yaml
Read Operations:
  1. Determine classification (global vs project)
  2. Read appropriate CLAUDE.md file
  3. Parse existing MANUS sections
  4. Preserve append-only structure

Write Operations:
  1. Generate timestamp: ISO 8601 format
  2. Apply stable prefix: 🕐 [Timestamp] [Type Icon]
  3. Append to appropriate section
  4. Never modify existing entries
  5. Add cache optimization comments

Allowed Tools:
  - Read: For reading CLAUDE.md files
  - Write: For creating new sections
  - Edit: For appending to existing sections
  - Grep: For searching existing patterns
```

### 5.2 Cache Optimization Strategy

```yaml
Stable Prefixes:
  Format: "🕐 [ISO 8601 Timestamp] [Icon] [Type]: "
  Example: "🕐 2025-10-23T14:30:00 🎯 Focus: "

  Rationale:
    - Timestamp first → stable prefix for all entries
    - Icon second → visual scanning
    - Type third → semantic grouping

Append-Only Updates:
  - Never modify previous entries
  - Status changes append new entry
  - Reference previous entry by timestamp
  - Complete history preserved

Cache Breakpoint Management:
  - Add explicit cache breakpoint comments
  - Group related entries together
  - Minimize mid-section variations
```

### 5.3 Recoverable Compression

```yaml
File Path References:
  Instead of: [Full file content]
  Use: 🔗 Related Files: /path/to/file.ts:123

  Rationale:
    - Preserve restoration path
    - Reduce token usage
    - Maintain KV-cache efficiency

URL References:
  Instead of: [Full web content]
  Use: 🔗 References: https://docs.example.com/article

  Rationale:
    - Content recoverable via URL
    - Compress verbose web content
    - Preserve learning signal

Code Snippets:
  Keep: Error stack traces (learning signal)
  Keep: Solution code (reusability)
  Compress: Large file contents → file paths
```

---

## 6. Migration Strategy

### 6.1 Existing Data Migration

```yaml
Step 1: Backup Current Data
  - Backup ~/.claude/CLAUDE.md
  - Backup .claude/CLAUDE.md (old system level)
  - Backup CLAUDE.md (project level)

Step 2: Content Analysis
  - Read all C.md entries from both levels
  - Read all X.md entries from both levels
  - Read all Z.md entries from both levels
  - Classify each entry: global vs project

Step 3: Section Mapping
  C.md FOCUS → MANUS FOCUS
  C.md TODO → MANUS TODO
  C.md PROCESS → MANUS PROCESS
  X.md ERROR → MANUS ERROR (with RECOVERY/ADAPTATION merged)
  X.md PATTERNS → MANUS PATTERNS
  Z.md EXPERIENCES + SOLUTIONS → MANUS SUCCESS
  Z.md INSIGHTS + TECHNIQUES → MANUS INSIGHTS
  Z.md PATTERNS → MANUS PATTERNS (merge with X patterns)

Step 4: Write to New Structure
  - Write global entries to ~/.claude/CLAUDE.md
  - Write project entries to CLAUDE.md
  - Preserve timestamps and append-only order
  - Add migration markers

Step 5: Cleanup
  - Archive old .claude/CLAUDE.md
  - Update CLAUDE.md references
  - Delete C/X/Z command files
  - Create new MANUS.md command
```

### 6.2 Command Reference Updates

```yaml
Files to Update:
  - ~/.claude/CLAUDE.md (machine level doc)
    Remove: Three-tier system description
    Add: Dual-tier system description
    Update: Command list (remove C/X/Z, add MANUS)

  - CLAUDE.md (project level doc)
    Remove: System level references
    Update: Command list
    Add: MANUS usage examples

  - Other commands referencing C/X/Z:
    Search for: "/C", "/X", "/Z" mentions
    Replace with: "/manus [type]" references
```

---

## 7. Quality Assurance

### 7.1 Validation Checklist

```yaml
Design Validation:
  ✅ MANUS principles integrated (KV-cache, error preservation, file-based context)
  ✅ Dual-tier classification clear and simple
  ✅ Seven sections consolidate original nine
  ✅ Append-only structure preserved
  ✅ Stable prefixes defined
  ✅ Recoverable compression specified

Implementation Validation:
  ✅ Command metadata complete
  ✅ Parameter templates defined
  ✅ File operations specified
  ✅ Cache optimization strategy clear
  ✅ Migration path defined
  ✅ Cleanup process documented

Documentation Validation:
  ✅ All design decisions explained
  ✅ Examples provided
  ✅ Migration strategy clear
  ✅ Quality assurance defined
```

### 7.2 Testing Strategy

```yaml
Unit Tests:
  - Test classification logic (global vs project)
  - Test timestamp generation
  - Test stable prefix formatting
  - Test section detection and parsing

Integration Tests:
  - Test read/write to CLAUDE.md files
  - Test append-only updates
  - Test pattern consolidation
  - Test recoverable compression

Migration Tests:
  - Test C.md → MANUS migration
  - Test X.md → MANUS migration
  - Test Z.md → MANUS migration
  - Test three-tier → dual-tier mapping
  - Verify no data loss

User Acceptance:
  - Verify dual-tier classification intuitive
  - Verify parameter templates clear
  - Verify command usage straightforward
  - Verify documentation complete
```

---

## 8. Success Criteria

```yaml
Technical Success:
  ✅ Single MANUS command replaces C/X/Z
  ✅ Dual-tier classification implemented
  ✅ MANUS principles integrated
  ✅ All existing data migrated
  ✅ No data loss during migration

User Success:
  ✅ Simpler classification (2 tiers vs 3)
  ✅ Unified command interface
  ✅ Clear parameter templates
  ✅ Complete documentation

Performance Success:
  ✅ Stable prefixes maximize cache reuse
  ✅ Append-only structure preserves determinism
  ✅ Recoverable compression reduces token usage
  ✅ File-based context enables unlimited memory
```

---

## 9. Timeline and Deliverables

```yaml
Phase 1: Design (COMPLETED)
  ✅ Create design document
  ✅ Define MANUS structure
  ✅ Specify dual-tier logic
  ✅ Define migration strategy

Phase 2: Implementation (NEXT)
  📝 Create MANUS.md command file
  📝 Implement classification logic
  📝 Implement parameter parsing
  📝 Implement file operations

Phase 3: Migration (AFTER)
  📝 Migrate existing C/X/Z data
  📝 Update CLAUDE.md references
  📝 Delete old command files
  📝 Test migration completeness

Phase 4: Validation (FINAL)
  📝 Run validation tests
  📝 User acceptance testing
  📝 Performance verification
  📝 Documentation review
```

---

## 10. References

```yaml
Production AI Systems:
  - MANUS Context Engineering Techniques
    Source: https://dev.to/olimdzhon/context-engineering-techniques-in-production-ai-agents-1hk9
    Key Topics: KV-cache optimization, error preservation, attention management

Claude Code Documentation:
  - Official Slash Commands Guide
  - Configuration Management
  - Best Practices

Existing Implementation:
  - .claude/commands/C.md (534 lines)
  - .claude/commands/X.md (757 lines)
  - .claude/commands/Z.md (741 lines)

Project Configuration:
  - ~/.claude/CLAUDE.md (machine level)
  - .claude/CLAUDE.md (system level - to be removed)
  - CLAUDE.md (project level)
```

---

## Appendix A: Complete Section Templates

### FOCUS Section Template
```markdown
## 🎯 FOCUS

### Active Attention Anchors

#### 🕐 2025-10-23T14:30:00 🎯 Current Focus: Implementing MANUS command
- 📊 Priority: HIGH
- ⏱️ Expected Duration: 4 hours
- 🎯 Success Criteria:
  - MANUS.md command created and functional
  - All C/X/Z data migrated
  - Documentation updated
- 🔗 Related Context:
  - PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md
  - .claude/commands/C.md (to be replaced)
- 💭 Rationale: Critical for context management system consolidation

<!-- Cache Breakpoint: Focus section updated -->
```

### TODO Section Template
```markdown
## 📋 TODO

### Task List (Attention Management)

#### 🕐 2025-10-23T14:30:00 ⭕ Task: Create MANUS.md command file
- 🏷️ Type: DEV
- 📊 Priority: HIGH
- 🎯 Completion Criteria:
  - Command metadata complete
  - All 7 sections implemented
  - Parameter parsing functional
- 🔗 Dependencies:
  - Design document completed (✅ Done)
- 📝 Notes: Use design spec from PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md
- **Status**: ⭕Pending

#### 🕐 2025-10-23T14:45:00 🔄 Task: Create MANUS.md command file
- **Status**: ⭕Pending → 🔄InProgress

<!-- Cache Breakpoint: TODO section updated -->
```

### ERROR Section Template
```markdown
## ❌ ERROR

### Error Context Preservation

#### 🕐 2025-10-23T14:30:00 ❌ Error: Classification logic failed to handle edge case
- 🏷️ Type: LOGIC
- 📊 Severity: MEDIUM
- 🎯 Failed Action: Classifying context entry with both global and project indicators
- 📝 Full Context:
  ```
  Entry: "本项目使用通用的React最佳实践"
  Contains both: "本项目" (project) and "通用" (global)
  Classification: Failed with ambiguity error
  Expected: Default to project level per design spec
  ```
- 💡 Learning Value: Need explicit tie-breaker logic for ambiguous cases
- 🔗 Related Files:
  - .claude/commands/MANUS.md:145 (classification function)

##### 🔧 Recovery
- 🏷️ Strategy: REPAIR
- 📝 Steps:
  1. Add tie-breaker: If both indicators present, default to project level
  2. Add logging for ambiguous cases
  3. Update classification tests
- ⏱️ Recovery Time: 15 minutes

##### 🔄 Adaptation
- 📝 Root Cause: Design spec didn't cover ambiguous cases
- 🔧 Prevention Measures:
  - Added explicit tie-breaker logic
  - Updated design document with edge case handling
  - Added test cases for ambiguous inputs
- 📈 System Updates:
  - Classification logic updated
  - Test suite expanded

<!-- Cache Breakpoint: Error section updated -->
```

---

**END OF DESIGN DOCUMENT**

---

**Next Steps**:
1. Review and approve design document
2. Proceed to Phase 2: Implementation
3. Create MANUS.md command file
4. Begin migration process

**Design Sign-off**: Ready for implementation ✅
