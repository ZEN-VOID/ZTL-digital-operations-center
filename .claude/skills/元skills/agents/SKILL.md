---
name: agents
description: Design, create, and optimize Claude Code subagents based on 2025 prompt engineering and context engineering best practices. Use when building new intelligent agents or improving existing agent configurations.
---

# Claude Code Subagent Creation

Create high-performance, structured Claude Code subagents through systematic context engineering and component design.

## What Are Subagents?

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. Each subagent:

- ✅ Has a specific purpose and domain expertise
- ✅ Uses an **independent context window** separate from the main conversation
- ✅ Can be configured with **specific tool access**
- ✅ Contains **custom system prompts** guiding its behavior

**Key Benefits**:
- **Context Efficiency**: Protect main context for longer overall conversations
- **Specialization**: Optimized configuration and tool sets for specific tasks
- **Modularity**: Develop, test, and deploy independently

## When to Use This Skill

Use this skill to:

- Create new specialized subagents for specific domains
- Optimize existing subagent configurations
- Understand subagent architecture and best practices
- Design tool sets and guardrails for agents
- Build multi-agent collaboration systems

## Quick Start

### 1. Define Agent Value

Answer these core questions:

```yaml
Agent Goal: What is this agent's ultimate purpose?
Value Generation: How does it create value?
  - ProcessAutomation (automate workflows)
  - Derisking (reduce risk)
  - DataProcessing (handle data)
  - KnowledgeWork (knowledge tasks)
Domain: Which business domain does it serve?
  - Development
  - Operations
  - Content
  - Analysis
```

### 2. Design Interaction Architecture

```yaml
Interaction Mode:
  - Autonomous: Fully autonomous execution
  - HumanInTheLoop: Human approval for key decisions
  - RequestResponse: Passive response only

Agency Level:
  - StaticWorkflow: Follow fixed processes
  - ModelDrivenWorkflow: LLM dynamic workflow decisions
  - AdaptivePlanning: Agent autonomously plans and adjusts
```

**Decision Matrix**:
```
High Risk + High Complexity → HumanInTheLoop + ModelDrivenWorkflow
Low Risk + Low Complexity → Autonomous + StaticWorkflow
High Risk + Low Complexity → HumanInTheLoop + StaticWorkflow
Low Risk + High Complexity → Autonomous + ModelDrivenWorkflow
```

### 3. Plan Component Capabilities

#### Tools Configuration

Design principles:
- **Necessity Check**: Each tool must map to a clear task requirement
- **Complete Coverage**: Full chain from information gathering to execution
- **Error Handling**: Every tool should have a fallback strategy

Example tool set layers:
```yaml
Information Gathering Layer:
  - Read: Read file contents
  - Grep: Search code patterns
  - mcp__github_mcp__get_pull_request: Get PR details

Analysis Processing Layer:
  - Bash: Run static analysis tools
  - Python: Execute data processing

Execution Operation Layer:
  - Write: Create new files
  - Edit: Modify existing files
  - mcp__github_mcp__create_pull_request_review: Publish reviews
```

#### Memory System

```yaml
Short-term Memory (Conversation Memory):
  - Purpose: Maintain single conversation context
  - Implementation: Messages API message history
  - Capacity: Typically within 200K tokens

Long-term Memory (Persistent Memory):
  - Purpose: Cross-conversation knowledge accumulation
  - Implementation: External storage (database, vector store)
  - Examples: User preferences, historical decisions, knowledge graphs

Memory Strategies:
  - Compaction: Periodically summarize and compress old context
  - Structured Notes: Store structured notes rather than raw conversations
  - Reference-based: Store references rather than complete data
```

#### Guardrails Mechanism

```yaml
Guardrail Types:

1. Input Validation:
   - Parameter type checking
   - Permission verification
   - Malicious input filtering

2. Behavior Constraints:
   - "Never approve PR when tests fail"
   - "Never modify main branch code"
   - "Sensitive operations require human confirmation"

3. Output Control:
   - Sensitive information filtering
   - Format validation
   - Toxicity detection

4. Resource Limits:
   - API call rate limiting
   - Token consumption budget
   - Execution time caps
```

### 4. Build System Prompt

Structure based on the 10-element prompt system:

```markdown
---
name: [agent-name]
description: [One-sentence description of core capability]
tools: [tool-list]
model: inherit
---

# [Agent Name]

## Task Context (Role & Goals)
You are [role positioning], focused on [core goals]. Your main responsibility is [specific tasks].

## Tone Context (Communication Style)
In all interactions, you should [tone description].

## Task Description & Rules

### Core Tasks
[Specific task descriptions]

### Behavior Rules
1. [Rule 1]
2. [Rule 2]
...

### Boundary Conditions
- If [situation A], then [behavior A]
- If uncertain how to respond, [exit strategy]

## Examples

<example>
<user_request>
[User request example]
</user_request>

<agent_response>
[Agent response example]
</agent_response>
</example>

[More examples...]

## Precognition (Thinking Guidance)

Before executing tasks, use this thinking framework:

<scratchpad>
1. Analyze: Understand the core requirements of the request
2. Plan: Determine required tools and steps
3. Evaluate: Check compliance with guardrail rules
</scratchpad>

## Output Formatting

All responses should follow this format:
<response>
[Structured response content]
</response>
```

### 5. Create Subagent File

#### Official YAML Format

```yaml
---
name: your-sub-agent-name  # Required: unique identifier using lowercase and hyphens
description: Describe when this subagent should be invoked  # Required: natural language description
tools: tool1, tool2, tool3  # Optional: comma-separated list. Omit to inherit all tools
model: sonnet  # Optional: model alias (sonnet/opus/haiku) or 'inherit' to use main conversation model
---

Your subagent's system prompt goes here. This can span multiple paragraphs and should clearly
define the subagent's role, capabilities, and problem-solving approach.

Include specific instructions, best practices, and any constraints the subagent should follow.
```

#### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Unique identifier using lowercase and hyphens |
| `description` | ✅ | Natural language description of subagent purpose (for auto-delegation) |
| `tools` | ❌ | Comma-separated tool list. Omit to inherit all tools (including MCP tools) |
| `model` | ❌ | Model alias or 'inherit'. Omit to default to configured subagent model |

#### Tool Configuration Strategy

Two options for configuring tools:

1. **Omit tools field** (Recommended):
   - Inherits all tools from main thread, including MCP tools
   - Suitable for most general-purpose subagents

2. **Specify tool list** (Fine-grained control):
   ```yaml
   tools: Read, Write, Edit, Grep, Glob, Bash
   ```
   - Only grant necessary tools for improved security
   - Helps subagent focus on relevant operations
   - Can be edited via `/agents` interface

#### File Path & Naming Conventions

```yaml
Project-level subagent:
  Path: .claude/agents/[name].md
  Example: .claude/agents/code-reviewer.md
  Scope: Current project only
  Priority: Highest

User-level subagent:
  Path: ~/.claude/agents/[name].md
  Example: ~/.claude/agents/debugger.md
  Scope: All projects
  Priority: Lower

Naming Convention:
  - Use lowercase letters and hyphens (kebab-case)
  - Descriptive (e.g., github-pr-reviewer, data-scientist)
  - Avoid excessive length (2-4 words recommended)
```

### 6. Activate & Manage

**Method 1: Use `/agents` command (Recommended)**

```bash
/agents
```

This opens an interactive menu where you can:
- ✅ View all available subagents (built-in, user, and project)
- ✅ Create new subagents through guided setup
- ✅ Edit existing custom subagents, including tool access
- ✅ Delete custom subagents
- ✅ See which subagents are active when duplicates exist

**Method 2: Direct File Management**

```bash
# Create project subagent
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Proactively used to run tests and fix failures
---
You are a test automation expert. When you see code changes, proactively run appropriate tests.
If tests fail, analyze failures and fix them while maintaining original test intent.
EOF
```

## Core Principles (2025 Edition)

### Context Engineering > Prompt Engineering

> **Core Concept**: Shift from "finding perfect wording" to "configuring optimal context"

```yaml
Traditional Prompt Engineering:
  - Focus: Word choice, tone, format
  - Problem: Easily trapped in "alchemy"

New Context Engineering:
  - Focus: Minimize high-signal token sets
  - Goal: Maximize model behavior quality within limited attention budget
  - Principle: "Context is a finite resource with diminishing marginal returns"
```

**Practical Guidance**:
- ✅ Use XML tags to structure information
- ✅ Progressive context disclosure
- ✅ Just-in-time context retrieval
- ❌ Avoid redundant information stacking
- ❌ Avoid vague high-level instructions

### 10-Element Prompt System

```yaml
Element 1 - User Role (Required):
  Position: First message in Messages API
  Purpose: Initialize conversation role

Element 2 - Task Context (Core):
  Position: Beginning of prompt
  Content: Role positioning, overall goals, business domain
  Example: "You are an AI agent focused on GitHub PR review..."

Element 3 - Tone Context (Optional):
  Position: After Task Context
  Content: Expected interaction tone and style
  Example: "Maintain professional, friendly, constructive tone"

Element 4 - Task Description & Rules (Critical):
  Position: Middle
  Content: Specific task description, behavior rules, boundary conditions
  Principle: Logical clarity, clear definition, provide "exit mechanism"

Element 5 - Skills & Tool Dependencies (When Applicable):
  Position: After Task Description & Rules
  Purpose: Specify which skills the agent uses and when
  Content:
    - Skills the agent may invoke for execution
    - Boundaries between agent (decision-making) and skill (execution) responsibilities
    - When to call skills vs use built-in tools directly
  Principle: Agent focuses on orchestration and domain expertise, skills handle complex execution

  Usage Pattern:
    Agent-Only: "Use Read/Write/Edit tools to..." (no skills needed)
    Agent+Skills: "When users request X, use [skill-name] skill to..."

  Example:
    "When users request image generation:
     1. Optimize their prompt based on your expertise
     2. Use the text-to-image skill to generate the image
     3. The skill handles API communication and file management
     4. You focus on creative direction and quality assessment"

Element 6 - Examples (Most Powerful):
  Position: After Skills & Tool Dependencies
  Format: <example>...</example> XML tags
  Principle: "Examples > any other technique", more is better
  Types: Standard scenarios + edge cases + error handling

Element 7 - Input Data (Optional):
  Position: Flexible
  Format: XML tag encapsulation <data>...</data>
  Principle: Clear marking, structured, parseable

Element 8 - Immediate Task (Reminder):
  Position: Near end
  Content: Restate current specific task
  Reason: Maintain focus in long prompts

Element 9 - Precognition (Thinking Guidance):
  Position: After task request
  Content: "Think step-by-step before answering..."
  Applicable: Multi-step complex tasks

Element 10 - Output Formatting (Optional):
  Position: Near end
  Content: Expected output format
  Example: "Place response in <response> tags"
```

### Chain-of-Thought (CoT) Reasoning

```yaml
Basic CoT:
  Pattern: "Think step-by-step before answering"
  Applicable: Multi-step reasoning tasks

Advanced CoT:
  Pattern: "Use <scratchpad> for thinking, then <answer> for final response"
  Advantage: Separate thinking process from final output
  Example:
    <scratchpad>
      1. Analyze user request...
      2. Identify required components...
      3. Assess potential risks...
    </scratchpad>
    <answer>
      Based on analysis, recommend adopting...
    </answer>
```

## Extended Reference: Skills Integration Patterns

> **Note**: For basic skills integration concepts, see Element 5 in the 10-Element Prompt System above. This section provides detailed collaboration patterns and implementation examples.

### Collaboration Patterns

#### Pattern 1: One-to-One (Specialized Pairing)

```yaml
Structure: One agent → One dedicated skill

Example - AIGC Workflow:
  V3-AIGC Image Generator (Agent):
    Role: Creative direction, prompt optimization
    Skills Called: text-to-image skill

  V4-AIGC Image Editor (Agent):
    Role: Image modification guidance
    Skills Called: image-to-image skill

  V5-AIGC Image Analyzer (Agent):
    Role: Analysis framework
    Skills Called: image-recognition skill

Characteristics:
  - Clear separation of concerns
  - Agent provides domain expertise
  - Skill handles technical execution
  - Each skill is self-contained
```

#### Pattern 2: One-to-Many (Orchestration)

```yaml
Structure: One agent → Multiple skills

Example - Intelligence Analyst:
  E0-Intelligence Coordinator (Agent):
    Role: Task decomposition, workflow orchestration
    Skills Called:
      - web-scraping skill (data collection)
      - data-analysis skill (processing)
      - report-generation skill (output)

Characteristics:
  - Agent acts as orchestrator
  - Skills called in sequence or parallel
  - Each skill has specific responsibility
  - Agent integrates results
```

#### Pattern 3: Many-to-One (Shared Utility)

```yaml
Structure: Multiple agents → One shared skill

Example - Office Automation:
  Agents:
    - R1-Finance Manager (budget reports)
    - R2-HR Manager (employee rosters)
    - R4-Secretary (meeting notes)

  Shared Skill:
    - excel-data-processor skill

Characteristics:
  - Skill provides common capability
  - Multiple agents leverage same tool
  - Reduces code duplication
  - Centralized maintenance
```

### Designing Agents with Skills in Mind

When creating an agent that will use skills:

#### 1. In Agent System Prompt

```markdown
---
name: aigc-image-designer
description: AI image generation specialist using state-of-the-art models
tools: Read, Write, Edit, Bash
---

# AIGC Image Designer

## Role & Expertise
You are an AI image generation specialist who helps users create high-quality images
using advanced AI models. You provide creative direction and technical optimization.

## Core Capabilities

### 1. Creative Consultation
[Provide guidance on prompts, styles, composition...]

### 2. Image Generation
When users request image generation, use the **text-to-image skill**:
- Optimize user prompts for best results
- Select appropriate model and parameters
- Call the skill with optimized configuration
- Review and refine generated images

### 3. Technical Optimization
[Provide technical parameter recommendations...]

## Workflow Example

<example>
<user_request>Create a sunset landscape image</user_request>
<agent_process>
1. Analyze request and suggest style directions
2. Optimize prompt: "Serene sunset over mountain landscape, golden hour,
   dramatic clouds, cinematic lighting, photorealistic, 8K quality"
3. Recommend parameters: model=flux, size=1024x768
4. Call text-to-image skill with optimized configuration
5. Review result and suggest refinements if needed
</agent_process>
</example>

**Important**: You focus on creative direction and prompt optimization. The
text-to-image skill handles API communication and image generation.
```

#### 2. Define Clear Boundaries

```yaml
Agent Responsibilities:
  ✅ Domain expertise and decision-making
  ✅ Parameter optimization and validation
  ✅ Result interpretation and guidance
  ✅ User interaction and refinement

Skill Responsibilities:
  ✅ API/external system communication
  ✅ Error handling and retry logic
  ✅ Data transformation and processing
  ✅ Technical execution details
```

#### 3. Specify Skill Dependencies

In agent documentation or configuration:

```yaml
---
name: data-analyst
description: Data analysis specialist with visualization capabilities
tools: Read, Write, Edit, Bash, Grep, Glob
skill_dependencies:
  - data-pipeline: For ETL operations
  - chart-generator: For visualizations
  - excel-processor: For spreadsheet operations
---
```

### Real-World Examples

#### Example 1: AIGC Agent + Text-to-Image Skill

**Agent File** (`.claude/agents/V3-AIGC文生图设计师.md`):
```markdown
---
name: aigc-image-designer
description: AI image generation specialist
---

You are an AI image generation expert. When users need images:

1. Understand requirements (subject, style, mood, technical specs)
2. Optimize prompts for best generation results
3. Use the text-to-image skill for actual generation
4. Review and refine based on results

You provide creative direction; the skill handles execution.
```

**Skill File** (`.claude/skills/text-to-image/SKILL.md`):
```markdown
---
name: text-to-image
description: Generate images from text prompts using AI models
---

# Text-to-Image Generation

Generate images using advanced AI models (Flux, DALL-E, Stable Diffusion).

## Quick Start

```python
# Called by agents with optimized parameters
result = generate_image(
    prompt="optimized prompt text",
    model="flux",
    size="1024x768"
)
```

[Detailed configuration, API handling, scripts...]
```

**Execution Flow**:
```
User Request → V3 Agent (creative direction) → text-to-image skill (API call) → Generated Image
```

#### Example 2: Intelligence Agent + Multiple Skills

**Agent File** (`.claude/agents/E0-情报任务需求拆解员.md`):
```markdown
---
name: intelligence-coordinator
description: Intelligence gathering and analysis coordinator
---

You coordinate intelligence operations by:

1. Analyzing user requirements
2. Decomposing into subtasks
3. Calling appropriate skills in sequence:
   - web-scraping skill (data collection)
   - data-analysis skill (processing)
   - report-generation skill (output)
4. Integrating results into comprehensive reports
```

**Execution Flow**:
```
User Request → E0 Agent (orchestration) ┬→ web-scraping skill
                                        ├→ data-analysis skill
                                        └→ report-generation skill
                                        ↓
                                   Integrated Report
```

### Best Practices

1. **Keep Agents Focused**: Agent provides domain knowledge, skill provides execution
2. **Design for Reusability**: Skills should be agent-agnostic and reusable
3. **Document Dependencies**: Clearly state which skills an agent may use
4. **Maintain Boundaries**: Don't duplicate skill logic in agent prompts
5. **Test Independently**: Verify agent reasoning and skill execution separately

## Quality Checklist

Verify quality after creating agent using this checklist:

```yaml
□ Value Clarity
  - [ ] Agent Goal is clear and measurable
  - [ ] Value Generation maps to actual business value
  - [ ] Target users and use cases are clear

□ Role Positioning
  - [ ] Name is concise and descriptive
  - [ ] Description clearly states core capability in one sentence
  - [ ] Domain classification is accurate

□ Interaction Architecture
  - [ ] Interaction Mode matches risk level
  - [ ] Agency Level matches complexity
  - [ ] Human intervention points are clear (if applicable)

□ Tool Design
  - [ ] Each tool has a clear purpose
  - [ ] Tool set covers complete task chain
  - [ ] Tool names and descriptions are clear
  - [ ] Has fallback and error handling strategy

□ Memory System
  - [ ] Short-term memory scope is clear
  - [ ] Long-term memory (if needed) has storage plan
  - [ ] Memory compression strategy (if needed) is defined

□ Guardrails Mechanism
  - [ ] Input validation rules are complete
  - [ ] Behavior constraints are specific and executable
  - [ ] Output control measures are in place
  - [ ] Resource limits are reasonable

□ System Prompt Quality
  - [ ] Includes all necessary prompt elements
  - [ ] Uses XML tags to structure information
  - [ ] Provides at least 2-3 examples
  - [ ] Examples cover standard scenarios and edge cases
  - [ ] Includes thinking framework (Precognition)
  - [ ] Output format is clearly defined

□ Skills Integration (if applicable)
  - [ ] Clearly identifies which skills the agent uses
  - [ ] Defines boundaries between agent and skill responsibilities
  - [ ] Documents skill dependencies in agent configuration
  - [ ] Agent focuses on decision-making, skills handle execution
  - [ ] Skills are agent-agnostic and reusable

□ File Specifications
  - [ ] YAML front matter format is correct
  - [ ] Filename follows naming conventions
  - [ ] Stored in correct path (.claude/agents/)
  - [ ] All tools in Tools list are available

□ Testing Verification
  - [ ] Test response quality with example scenarios
  - [ ] Verify tool calls are correct
  - [ ] Check guardrail rules are effective
  - [ ] Confirm interaction mode meets expectations
```

## Best Practices

### 1. Start with Claude-Generated Subagents

**Strongly Recommended**: Use Claude to generate your initial subagent, then iterate to personalize it. This approach gives the best results - a solid foundation you can customize for specific needs.

### 2. Design Focused Subagents

Create subagents with **single, clear responsibilities** rather than trying to make one subagent do everything. This improves performance and makes subagents more predictable.

### 3. Write Detailed Prompts

Include **specific instructions, examples, and constraints** in your system prompt. The more guidance you provide, the better the subagent will perform.

### 4. Limit Tool Access

Only grant tools **necessary** for the subagent's purpose. This improves security and helps the subagent focus on relevant operations.

### 5. Version Control

**Check project subagents into version control** so your team can benefit from and collaborate on improving them.

## Invocation Methods

### Auto-Delegation

Claude Code **proactively** delegates tasks based on:
- Task description in your request
- `description` field in subagent configuration
- Current context and available tools

### Explicit Invocation

Request a specific subagent by mentioning it in your command:

```
> Use test-runner subagent to fix failing tests
> Let code-reviewer subagent review my recent changes
> Ask debugger subagent to investigate this error
```

### Chaining Subagents

For complex workflows, chain multiple subagents:

```
> First use code-analyzer subagent to find performance issues, then use optimizer subagent to fix them
```

## Performance Considerations

### Advantages

- **Context Efficiency**: Subagents help protect main context for longer overall conversations

### Trade-offs

- **Latency**: Subagents start from a clean state each time invoked, potentially adding latency as they need to gather context to complete work effectively

## Reference Resources

### Official Documentation

- **[Claude Code Subagents Official Docs](https://docs.claude.com/zh-CN/docs/claude-code/sub-agents)** ⭐ Must-read
- [Anthropic Prompt Engineering Course](https://github.com/anthropics/courses)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

**Version**: 1.0.0
**Compatible With**: Claude Code v4.5+, Sonnet 4.5
**Based On**: Claude Code Official Documentation (2025-10-18)
