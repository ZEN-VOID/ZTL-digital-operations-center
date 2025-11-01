---
name: Figma Batch Replace
description: Batch replace images in Figma with task orchestration, progress tracking, and retry mechanisms. Use when batch updating images, 6-batch production workflows, or when user mentions batch replace, bulk update, or template automation. Requires Figma API token and backend API.
---

# Figma Batch Replace

## Quick Start

### Replace single image
```python
import sys
sys.path.append('./plugins/创意组/skills/figma/batch-replace-v2/scripts')
from batch_replace_client import BatchReplaceClient

async with BatchReplaceClient() as client:
    task = await client.create_task(
        file_key="YOUR_FILE_KEY",
        replacements=[{
            "node_id": "123:456",
            "image_url": "https://example.com/new-image.jpg"
        }]
    )
    print(f"Task ID: {task['task_id']}")
```

### 6-Batch Production Workflow
```bash
# Classic restaurant 6-dish batch workflow
python scripts/six_batch_workflow.py \
  --template-file YOUR_FILE_KEY \
  --dishes-json dishes.json \
  --output-dir ./batches
```

## Documentation

- **[API Reference](reference.md)**: Complete batch replace API documentation
- **[6-Batch Guide](six-batch-guide.md)**: Detailed guide for 6-dish batch production
- **[Examples](examples.md)**: Common batch replace scenarios

## Bundled Scripts

- **`scripts/batch_replace_client.py`**: Core batch replace operations
- **`scripts/six_batch_workflow.py`**: 6-dish batch production automation
- **`scripts/monitor_task.py`**: Real-time task monitoring
- **`scripts/retry_failed.py`**: Retry failed replacements

## Requirements

```bash
pip install httpx backoff pydantic-settings
export FIGMA_API_TOKEN=your_token_here
export BATCH_API_ENDPOINT=http://localhost:8000
```

## Related Skills

- For file management: See `../file-management-v2/SKILL.md`
- For workflow orchestration: See `../workflow-orchestration-v2/SKILL.md`
