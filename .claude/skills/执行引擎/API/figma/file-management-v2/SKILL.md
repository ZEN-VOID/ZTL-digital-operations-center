---
name: Figma File Management
description: Retrieve Figma file information, query node details, get version history, navigate document structure. Use when working with Figma files, analyzing design structure, or when user mentions Figma documents, file structure, nodes, layers, or version control. Requires Figma API token.
---

# Figma File Management

## Quick Start

### Get file information
```python
# Import the client
import sys
sys.path.append('./.claude/skills/figma/file-management-v2/scripts')
from figma_file_client import FigmaFileClient

# Use the client
async with FigmaFileClient() as client:
    file_data = await client.get_file(file_key="YOUR_FILE_KEY")
    print(f"File: {file_data['name']}")
    print(f"Last modified: {file_data['lastModified']}")
```

### Get specific nodes
```python
async with FigmaFileClient() as client:
    nodes = await client.get_file_nodes(
        file_key="YOUR_FILE_KEY",
        node_ids=["123:456", "789:012"]
    )
    for node_id, node_data in nodes['nodes'].items():
        print(f"Node: {node_data['document']['name']}")
```

### Get version history
```python
async with FigmaFileClient() as client:
    versions = await client.get_file_versions(file_key="YOUR_FILE_KEY")
    for version in versions['versions']:
        print(f"{version['label']}: {version['created_at']}")
```

## Documentation

This skill provides comprehensive file management capabilities:

- **[API Reference](reference.md)**: Complete API documentation for all file operations
- **[Examples](examples.md)**: Detailed examples for common tasks and restaurant industry use cases

## Bundled Scripts

- **`scripts/figma_file_client.py`**: Core Figma file operations client
- **`scripts/traverse_nodes.py`**: Node traversal and structure analysis utilities
- **`scripts/find_nodes.py`**: Node search and filtering utilities

## Common Tasks

### Navigate document structure
Use the `traverse_nodes.py` script:
```bash
python scripts/traverse_nodes.py --file-key YOUR_FILE_KEY
```

### Find nodes by type or name
Use the `find_nodes.py` script:
```bash
# Find all FRAME nodes
python scripts/find_nodes.py --file-key YOUR_FILE_KEY --type FRAME

# Find nodes with name containing "菜品"
python scripts/find_nodes.py --file-key YOUR_FILE_KEY --pattern "菜品"
```

## Requirements

```bash
# Python dependencies
pip install httpx backoff pydantic-settings

# Environment variables
export FIGMA_API_TOKEN=your_token_here
```

## Error Handling

Common errors:
- **401 Unauthorized**: Invalid or missing API token
- **403 Forbidden**: No access to file
- **404 Not Found**: File or nodes not found
- **429 Rate Limited**: Too many requests (automatic retry with backoff)

See [reference.md](reference.md) for detailed error handling strategies.

## Related Skills

- For image export: See `../image-export/SKILL.md`
- For batch operations: See `../batch-replace/SKILL.md`
- For workflow automation: See `../workflow-orchestration/SKILL.md`
