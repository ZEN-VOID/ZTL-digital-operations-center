name: "Base PRP Template v3 - Multi-Channel Execution with Auto Task Management"
description: |

## Purpose
Template optimized for AI agents to implement features with multi-channel parallel execution and automatic task management activation. Includes context-rich validation and self-validation capabilities.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Multi-Channel Execution**: Enable parallel processing across multiple execution channels
3. **Auto Task Management**: Automatically activate TodoWrite task manager during execution phase
4. **Validation Loops**: Provide executable tests/lints the AI can run and fix
5. **Information Dense**: Use keywords and patterns from the codebase
6. **Progressive Success**: Start simple, validate, then enhance
7. **Global rules**: Be sure to follow all rules in CLAUDE.md

## Execution Framework
### Multi-Channel Configuration
- **Creation Phase**: Allow multiple agent channels for research, planning, and setup
- **Execution Phase**: Enable parallel task execution with automatic task manager activation
- **Validation Phase**: Coordinate multi-channel testing and verification

---

## Goal
[What needs to be built - be specific about the end state and desires]

## Why
- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]
  
- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]
  
- doc: [Library documentation URL] 
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [PRPs/ai_docs/file.md]
  why: [docs that the user has pasted in to the project]

```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
```bash

```

### Desired Codebase tree with files to be added and responsibility of file
```bash

```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: [Library name] requires [specific setup]
# Example: FastAPI requires async functions for endpoints
# Example: This ORM doesn't support batch inserts over 1000 records
# Example: We use pydantic v2 and  
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.
```python
Examples: 
 - orm models
 - pydantic models
 - pydantic schemas
 - pydantic validators

```

### Task Management and Execution Strategy

#### Auto-Activation Rules
```yaml
PRP_EXECUTION_CONFIG:
  creation_phase:
    multi_channel: true
    max_channels: 3
    auto_todo: false

  execution_phase:
    multi_channel: true
    max_channels: 5
    auto_todo: true
    todo_trigger: "IMMEDIATE"

  validation_phase:
    multi_channel: true
    max_channels: 2
    auto_todo: true
```

#### Task Breakdown with Channel Assignment
```yaml
Task 1: [Channel: Research/Setup]
RESEARCH and SETUP:
  - FIND pattern: "class OldImplementation"
  - ANALYZE existing architecture
  - DOCUMENT dependencies and constraints

Task 2: [Channel: Implementation-A]
MODIFY src/existing_module.py:
  - INJECT after line containing "def __init__"
  - PRESERVE existing method signatures
  - PARALLEL execution with Task 3

Task 3: [Channel: Implementation-B]
CREATE src/new_feature.py:
  - MIRROR pattern from: src/similar_feature.py
  - MODIFY class name and core logic
  - PARALLEL execution with Task 2

Task 4: [Channel: Testing]
VALIDATION and TESTING:
  - RUN validation suite
  - COORDINATE with implementation channels
  - ENSURE all tests pass

...(Continue with channel-specific task assignments...)

Task N: [Channel: Integration]
FINAL INTEGRATION:
  - MERGE all channel outputs
  - VERIFY system coherence
  - COMPLETE final validation
```


### Per task pseudocode as needed added to each task
```python

# Task 1
# Pseudocode with CRITICAL details dont write entire code
async def new_feature(param: str) -> Result:
    # PATTERN: Always validate input first (see src/validators.py)
    validated = validate_input(param)  # raises ValidationError
    
    # GOTCHA: This library requires connection pooling
    async with get_connection() as conn:  # see src/db/pool.py
        # PATTERN: Use existing retry decorator
        @retry(attempts=3, backoff=exponential)
        async def _inner():
            # CRITICAL: API returns 429 if >10 req/sec
            await rate_limiter.acquire()
            return await external_api.call(validated)
        
        result = await _inner()
    
    # PATTERN: Standardized response format
    return format_response(result)  # see src/utils/responses.py
```

### Integration Points
```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"
  
CONFIG:
  - add to: config/settings.py
  - pattern: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"
  
ROUTES:
  - add to: src/api/routes.py  
  - pattern: "router.include_router(feature_router, prefix='/feature')"
```

## Execution Control & Task Management

### Auto-Task Manager Activation
```yaml
EXECUTION_TRIGGER:
  phase: "execution"
  condition: "PRP_EXECUTION_PHASE_START"
  action: |
    # 自动激活任务管理器
    TodoWrite: ACTIVATE
    multi_channel: ENABLE
    parallel_execution: TRUE

AUTO_TODO_RULES:
  - trigger: "TASK_START"
    action: "CREATE_TODO_ITEM"
    status: "in_progress"

  - trigger: "TASK_COMPLETE"
    action: "MARK_COMPLETED"
    next_action: "START_NEXT_PARALLEL_TASK"

  - trigger: "VALIDATION_REQUIRED"
    action: "CREATE_VALIDATION_TODO"
    channel: "testing"
```

### Multi-Channel Coordination Protocol
```bash
# Channel synchronization during execution
PARALLEL_EXECUTION_START:
  - Channel-1: Implementation tasks
  - Channel-2: Testing preparation
  - Channel-3: Documentation updates

SYNC_POINTS:
  - After each major task completion
  - Before validation phases
  - At integration milestones
```

## Validation Loop

### Level 1: Syntax & Style (Auto-Managed)
```bash
# Auto-triggered via task manager - fix any errors before proceeding
ruff check src/new_feature.py --fix  # Auto-fix what's possible
mypy src/new_feature.py              # Type checking

# Expected: No errors. If errors, READ the error and fix.
# Task manager auto-tracks validation status
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns
```python
# CREATE test_new_feature.py with these test cases:
def test_happy_path():
    """Basic functionality works"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """Invalid input raises ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """Handles timeouts gracefully"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# Run and iterate until passing:
uv run pytest test_new_feature.py -v
# If failing: Read error, understand root cause, fix code, re-run (never mock to pass)
```

### Level 3: Integration Test
```bash
# Start the service
uv run python -m src.main --dev

# Test the endpoint
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs at logs/app.log for stack trace
```

## Final validation Checklist
- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

---

## Anti-Patterns to Avoid
- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"  
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific