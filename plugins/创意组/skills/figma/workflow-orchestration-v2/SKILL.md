---
name: Figma Workflow Orchestration
description: Orchestrate complex multi-step Figma workflows with parallel execution, dependency management, and status monitoring. Use when automating complex production processes, managing multi-batch workflows, or when user mentions workflow automation, task orchestration, or production pipelines. Requires backend API.
---

# Figma Workflow Orchestration

## Quick Start

### Create simple workflow
```python
import sys
sys.path.append('./plugins/创意组/skills/figma/workflow-orchestration-v2/scripts')
from workflow_client import WorkflowClient

async with WorkflowClient() as client:
    workflow = await client.create_workflow(
        name="Menu Production",
        steps=[
            {"action": "batch_replace", "file_key": "abc123"},
            {"action": "export_images", "depends_on": ["batch_replace"]}
        ]
    )
    print(f"Workflow ID: {workflow['workflow_id']}")
```

### Monitor workflow
```bash
python scripts/monitor_workflow.py --workflow-id WORKFLOW_ID
```

## Documentation

- **[API Reference](reference.md)**: Complete workflow orchestration API
- **[Workflow Patterns](patterns.md)**: Common workflow patterns and templates
- **[Examples](examples.md)**: Real-world workflow examples

## Bundled Scripts

- **`scripts/workflow_client.py`**: Core workflow operations
- **`scripts/monitor_workflow.py`**: Real-time workflow monitoring
- **`scripts/parallel_workflows.py`**: Execute workflows in parallel

## Requirements

```bash
pip install httpx backoff pydantic-settings asyncio
export WORKFLOW_API_ENDPOINT=http://localhost:8000
```

## Related Skills

- For batch operations: See `../batch-replace-v2/SKILL.md`
- For file management: See `../file-management-v2/SKILL.md`
