---
name: output-styles
description: Design, create, and optimize Claude Code output styles based on official specifications and user experience best practices. Use when customizing output formats, creating style templates, or optimizing output experience.
---

# Claude Code Output Styles Creation

Create efficient output style configurations that customize Claude's response format, structure, tone, and detail level for different scenarios.

## What Are Output Styles?

Output styles are Claude Code's configuration system for customizing output formats. Each output style:

- ✅ Defines specific output format and structure
- ✅ Supports multiple formats (Markdown, JSON, XML, tables)
- ✅ Configures tone, detail level, and organization
- ✅ Contains custom system prompts to guide output behavior

**Key Benefits**:
- **Consistency**: Ensure uniform output format across different scenarios
- **Readability**: Optimize structure to improve information retrieval efficiency
- **Customization**: Adjust style and detail level based on specific needs

## When to Use This Skill

Use this skill to:

- Create new output styles for specific scenarios
- Optimize existing style configurations
- Understand style architecture and format design
- Configure format, tone, and detail level
- Build reusable output templates

## Output Style Architecture

Output styles are stored as Markdown files with YAML front matter in three tiers:

| Tier | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project-level** | `.claude/output-styles/` | Current project | Highest ⭐⭐⭐ |
| **CLI-level** | `--output-styles` JSON parameter | Current session | Medium ⭐⭐ |
| **User-level** | `~/.claude/output-styles/` | All projects | Lower ⭐ |

**Naming Conflict Rules**: Project-level styles override CLI-level, which override user-level.

## Quick Start

### 1. Analyze Requirements

Answer these core questions:

```yaml
Target Scenario: What scenario will this output style be used for?
  Examples:
    - Code review reports
    - Data analysis results
    - Document generation
    - API responses

Output Format: What is the expected output format?
  Options:
    - Markdown (readable, structured, rich text)
    - JSON (machine-readable, structured, parseable)
    - XML (structured, nested, semantic)
    - Table (comparison-friendly, scannable)

Detail Level: How detailed should the information be?
  Options:
    - Concise (key results only)
    - Standard (balanced)
    - Detailed (complete context)

Tone and Style: What is the expected interaction style?
  Options:
    - Professional (formal, objective, precise)
    - Friendly (approachable, conversational)
    - Educational (step-by-step, explanatory)
    - Technical (concise, code-oriented)

Target Audience: Who will read these outputs?
  Options:
    - Developers
    - Product managers
    - End users
    - Systems/machines
```

### 2. Design Format Structure

#### Hierarchical Structure Design

```yaml
Classic Three-Layer Structure:

  Layer 1 - Overview:
    Content: Executive summary, key metrics, overall status
    Purpose: Quick understanding of the overall situation
    Example:
      # Code Review Report
      **Overall Score**: 8.5/10 ✅
      **Total Issues**: 12 (3 critical, 5 moderate, 4 minor)
      **Recommended Priority**: High

  Layer 2 - Details:
    Content: Categorized issues, specific locations, detailed explanations
    Purpose: Provide complete context and details
    Example:
      ## Critical Issues
      ### 1. Potential SQL Injection Risk
      **Location**: user_controller.py:45
      **Issue**: Direct concatenation of user input to SQL statement
      **Impact**: High-risk security vulnerability
      **Fix Recommendation**: Use parameterized queries

  Layer 3 - Actions:
    Content: Next steps, priority sorting, resource links
    Purpose: Guide subsequent actions
    Example:
      ## Recommended Actions
      1. 🔴 Fix Immediately: SQL injection risk (est. 15 min)
      2. 🟡 Optimize Soon: Performance improvements (est. 2 hours)
      3. 🟢 Long-term: Code refactoring suggestions (est. 1 day)
```

#### Visual Elements Design

```yaml
Icons and Symbols:
  Status Indicators:
    ✅ Success/Pass
    ❌ Failure/Error
    ⚠️ Warning/Caution
    ℹ️ Information/Tip
    🔴 High Priority
    🟡 Medium Priority
    🟢 Low Priority

  Data Indicators:
    📊 Statistics
    📈 Trending Up
    📉 Trending Down
    💡 Suggestion/Insight
    🔧 Fix Solution
    📝 Description/Documentation

Separation and Organization:
  Horizontal Separator: ---
  Section Separator: ===
  List Indent: - / 1. / •
  Code Block: ```language
  Quote Block: >
  Table: | Column | Column |

Color and Emphasis:
  Bold: **important content**
  Italic: *emphasized content*
  Inline Code: `code`
  Link: [text](url)
```

### 3. Write System Prompt

Build the system prompt based on output format specifications:

```markdown
---
name: [style-name]
description: [One-sentence description of output scenario and format]
---

# [Output Style Name]

## Output Format Specification

Organize all output content according to the following format:

### Structure Requirements
[Define output hierarchy and section organization]

### Format Rules
[Define Markdown/JSON/XML format usage specifications]

### Tone and Style
[Define communication tone, professionalism, vocabulary choices]

### Detail Level
[Define information density, expansion depth, example quantity]

## Output Template

<template>
[Provide specific output template example]
</template>

## Format Examples

<example>
<scenario>[Scenario description]</scenario>
<output>
[Output example following specification format]
</output>
</example>

## Important Notes

1. [Key format requirement 1]
2. [Key format requirement 2]
...
```

### 4. Create Configuration File

#### Official YAML Front Matter Format

```yaml
---
name: your-output-style-name  # Required: unique identifier using lowercase and hyphens
description: Describe when this output style should be used  # Required: natural language description
---

Your output style's system prompt goes here. This should clearly define
the format, structure, tone, and detail level requirements of the output.

Include specific format specifications, template examples, and any constraints.
```

**Configuration Fields**:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Unique identifier using lowercase and hyphens |
| `description` | ✅ | Natural language description of style purpose |

#### File Path and Naming Conventions

```yaml
Project-level output style:
  Path: .claude/output-styles/[name].md
  Example: .claude/output-styles/code-review-report.md
  Scope: Current project only
  Priority: Highest

User-level output style:
  Path: ~/.claude/output-styles/[name].md
  Example: ~/.claude/output-styles/technical-doc.md
  Scope: All projects
  Priority: Lower

Naming Convention:
  - Use lowercase letters and hyphens (kebab-case)
  - Descriptive (e.g., code-review-report, api-response)
  - Avoid excessive length (2-4 words recommended)
```

### 5. Test and Optimize

```yaml
□ Format Validation
  - [ ] YAML front matter format correct (--- at start and end)
  - [ ] name field uses lowercase and hyphens
  - [ ] description field clearly describes use case

□ Output Quality Testing
  - [ ] Test output format with different content types
  - [ ] Verify structure is clear and readable
  - [ ] Check detail level is appropriate
  - [ ] Confirm tone and style are consistent

□ Usability Verification
  - [ ] Apply in real scenarios
  - [ ] Collect user feedback
  - [ ] Identify improvement opportunities
```

## Core Concepts

### Common Output Format Types

```yaml
Markdown Format:
  Advantages: Readable, structured, rich text support
  Use Cases:
    - Document generation
    - Report output
    - Analysis result display
  Example:
    # Title
    ## Section
    - List item
    **Bold** *Italic*

JSON Format:
  Advantages: Machine-readable, structured, parseable
  Use Cases:
    - API responses
    - Data exchange
    - Configuration files
  Example:
    {
      "status": "success",
      "data": {...}
    }

XML Format:
  Advantages: Structured, nested, semantically clear
  Use Cases:
    - Configuration management
    - Data transmission
    - Document markup
  Example:
    <response>
      <status>success</status>
      <data>...</data>
    </response>

Table Format:
  Advantages: Clear comparison, easy scanning
  Use Cases:
    - Data comparison
    - List display
    - Statistical reports
  Example:
    | Col1 | Col2 | Col3 |
    |------|------|------|
    | Val1 | Val2 | Val3 |
```

### Output Detail Levels

```yaml
Concise Mode:
  Features: Core information only, highly compressed
  Use Cases: Quick queries, status checks
  Example: "✅ Success - 3 files updated"

Standard Mode:
  Features: Balance detail with readability
  Use Cases: Regular operations, general Q&A
  Example:
    Operation Result: Success
    Updated Files: file1.py, file2.js, file3.md
    Time Taken: 2.3 seconds

Detailed Mode:
  Features: Complete context, thorough explanation
  Use Cases: Complex analysis, educational explanations
  Example:
    ## Operation Execution Report

    ### Execution Overview
    - Status: ✅ Success
    - Start Time: 2025-10-18 10:30:00
    - End Time: 2025-10-18 10:30:02
    - Total Time: 2.3 seconds

    ### File Change Details
    1. file1.py
       - Operation: Update
       - Lines Changed: 15
       - Affected Functions: calculateTotal, validateInput
```

### Tone and Style

```yaml
Professional Style:
  Features: Formal, objective, precise
  Vocabulary: Technical terms, standardized expressions
  Example: "Based on analysis results, recommend adopting Strategy A to optimize performance metrics."

Friendly Style:
  Features: Approachable, conversational, accessible
  Vocabulary: Everyday language, analogies
  Example: "Good news! We found a great solution that can make the program run faster."

Educational Style:
  Features: Step-by-step, detailed explanations, rich examples
  Vocabulary: Concept explanations, principle descriptions
  Example: "First, we need to understand what caching is. Cache is like a quick-access notepad..."

Technical Style:
  Features: Concise, precise, code-oriented
  Vocabulary: Code snippets, technical details
  Example:
    ```python
    def optimize():
        cache.set(key, value, ttl=3600)
        return cache.get(key)
    ```
```

## Complete Examples

### Example 1: Code Review Report Style

`.claude/output-styles/code-review-report.md`:

```markdown
---
name: code-review-report
description: Structured report output format for code review scenarios, including issue classification, severity assessment, and specific fix recommendations
---

# Code Review Report Output Style

## Output Format Specification

Organize code review reports according to the following format:

### Structure Requirements

1. **Review Overview** - Provide high-level executive summary
2. **Detailed Analysis** - List issues by severity
3. **Best Practices** - Acknowledge good code practices
4. **Recommended Actions** - Provide priority-sorted action list

### Format Rules

- Use Markdown format
- Use heading levels (#, ##, ###) to organize content
- Use emoji icons to enhance readability
- Use lists and tables for structured information
- Use code blocks for code snippets

### Tone and Style

- Maintain professional but constructive tone
- Provide solutions when pointing out issues
- Acknowledge good practices
- Use clear, actionable language

### Detail Level

- Each issue includes: location, issue description, impact, fix recommendation
- Provide specific code examples
- Indicate priority and estimated fix time

## Output Template

```
# Code Review Report

## 📊 Review Overview

**Overall Score**: [score]/10 [status icon]
**Review Time**: [timestamp]
**Total Issues**: [count] ([critical] critical, [moderate] moderate, [minor] minor)
**Recommended Priority**: [High/Medium/Low]

## 🔍 Detailed Analysis

### 🔴 Critical Issues (if any)

#### 1. [Issue Title]
**Location**: [filename:line]
**Issue**: [detailed description]
**Impact**: [scope and severity]
**Fix Recommendation**:
```[language]
[suggested code fix]
```

### 🟡 Moderate Issues (if any)

[same format]

### 🟢 Minor Issues (if any)

[same format]

## ✅ Best Practices

[list praiseworthy code practices]

## 🚀 Recommended Actions

1. 🔴 Fix Immediately: [issue] (est. [time])
2. 🟡 Optimize Soon: [issue] (est. [time])
3. 🟢 Long-term Plan: [issue] (est. [time])
```

## Format Example

<example>
<scenario>Review Python code containing security vulnerability and performance issues</scenario>
<output>
# Code Review Report

## 📊 Review Overview

**Overall Score**: 6.5/10 ⚠️
**Review Time**: 2025-10-18 10:30:00
**Total Issues**: 5 (1 critical, 2 moderate, 2 minor)
**Recommended Priority**: High

## 🔍 Detailed Analysis

### 🔴 Critical Issues

#### 1. Potential SQL Injection Risk
**Location**: user_controller.py:45
**Issue**: Direct concatenation of user input to SQL statement, SQL injection risk exists
**Impact**: High-risk security vulnerability, may lead to data leakage or tampering
**Fix Recommendation**:
```python
# Current code (unsafe)
query = f"SELECT * FROM users WHERE username = '{username}'"

# Recommended change (safe)
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### 🟡 Moderate Issues

#### 1. Repeated Database Queries in Loop
**Location**: order_processor.py:78-85
**Issue**: Executing separate database query for each order in loop, N+1 query problem
**Impact**: Inefficient performance, significantly slower when processing many orders
**Fix Recommendation**:
```python
# Recommend using batch query
order_ids = [order.id for order in orders]
products = Product.objects.filter(id__in=order_ids)
```

## ✅ Best Practices

1. ✨ Good error handling mechanism (error_handler.py)
2. ✨ Comprehensive unit test coverage (test coverage: 85%)
3. ✨ Clear code comments and docstrings

## 🚀 Recommended Actions

1. 🔴 Fix Immediately: SQL injection risk (est. 30 min)
2. 🟡 Optimize Soon: N+1 query issue (est. 1 hour)
3. 🟢 Long-term Plan: Code refactoring for maintainability (est. 1 day)
</output>
</example>

## Important Notes

1. Always maintain objective and constructive tone
2. Each issue must include specific fix recommendations
3. Use emoji icons but avoid overuse
4. Code examples should clearly show "before" and "after" comparison
5. Priority assessment should be based on impact scope and severity
```

### Example 2: API Response JSON Style

`.claude/output-styles/api-response-json.md`:

```markdown
---
name: api-response-json
description: Standard JSON format for API responses, including status codes, data, error messages, and metadata
---

# API Response JSON Format

## Output Format Specification

All API responses should follow this JSON structure:

```json
{
  "status": "success|error",
  "code": 200,
  "message": "Operation description",
  "data": {
    // Response data
  },
  "meta": {
    "timestamp": "ISO 8601 timestamp",
    "request_id": "Unique request identifier",
    "version": "API version"
  },
  "errors": [
    {
      "field": "Field name",
      "message": "Error message",
      "code": "Error code"
    }
  ]
}
```

## Format Rules

1. Use valid JSON format
2. All responses include status and code fields
3. Success responses include data field
4. Error responses include errors array
5. Optionally include meta field for metadata

## Examples

<example>
<scenario>Successfully retrieve user information</scenario>
<output>
```json
{
  "status": "success",
  "code": 200,
  "message": "User information retrieved successfully",
  "data": {
    "user": {
      "id": "12345",
      "username": "johndoe",
      "email": "john@example.com"
    }
  },
  "meta": {
    "timestamp": "2025-10-18T10:30:00Z",
    "request_id": "req_abc123",
    "version": "v1"
  }
}
```
</output>
</example>

<example>
<scenario>Validation failure error</scenario>
<output>
```json
{
  "status": "error",
  "code": 400,
  "message": "Request validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format",
      "code": "INVALID_EMAIL"
    },
    {
      "field": "password",
      "message": "Password must be at least 8 characters",
      "code": "PASSWORD_TOO_SHORT"
    }
  ],
  "meta": {
    "timestamp": "2025-10-18T10:30:00Z",
    "request_id": "req_xyz789",
    "version": "v1"
  }
}
```
</output>
</example>
```

## Quality Checklist

After creating an output style, verify quality using this checklist:

```yaml
□ Format Clarity
  - [ ] Clear structure hierarchy
  - [ ] Reasonable information organization
  - [ ] Appropriate visual elements

□ Consistency
  - [ ] Unified format rules
  - [ ] Consistent tone and style
  - [ ] Standardized terminology

□ Readability
  - [ ] Easy to scan quickly
  - [ ] Key information highlighted
  - [ ] Examples sufficiently clear

□ Practicality
  - [ ] Meets actual needs
  - [ ] Easy to understand and apply
  - [ ] Provides actionable recommendations

□ File Specifications
  - [ ] YAML front matter format correct
  - [ ] Filename follows naming conventions
  - [ ] Stored in correct path

□ Testing Verification
  - [ ] Tested in real scenarios
  - [ ] Output quality meets expectations
  - [ ] Good user feedback
```

## Best Practices

### 1. Scenario-Driven Design

**Recommended**: Create dedicated output styles for different use scenarios rather than trying to adapt one style to all scenarios.

### 2. Maintain Simplicity

Create **clear, concise** format specifications. Overly complex formats reduce readability and usability.

### 3. Provide Ample Examples

Include **multiple examples** in the configuration, covering common scenarios and edge cases. Examples are the best format documentation.

### 4. Iterative Optimization

**Collect feedback** in actual use and continuously optimize format definitions and structural design.

### 5. Version Control

**Check project output styles into version control** so the team can share and collaborate on improving them.

## Invocation Methods

### Method 1: Specify in Conversation

```
User: "Please review this code using the code-review-report style"
```

### Method 2: As Default Style

Set default output style in project configuration (if supported).

### Method 3: Automatic Scenario Matching

Claude Code may automatically select appropriate output style based on task type.

## Reference Resources

### Official Documentation

- **[Claude Code Output Styles Official Docs](https://docs.claude.com/zh-CN/docs/claude-code/output-styles)** ⭐ Must-read
- [Claude Code Configuration Guide](https://docs.claude.com/zh-CN/docs/claude-code)

### Community Resources

- [Claude Code Templates](https://github.com/davila7/claude-code-templates)
- [Output Style Examples](https://github.com/anthropics/claude-code-examples)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-21
**Compatibility**: Claude Code v1.0+, Sonnet 4.5
**Based On**: Claude Code Official Documentation (2025-10-18)
