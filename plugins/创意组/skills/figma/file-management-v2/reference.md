# Figma File Management API Reference

Complete API documentation for Figma file operations.

## Table of Contents

- [File Operations](#file-operations)
- [Node Operations](#node-operations)
- [Version Operations](#version-operations)
- [Node Types Reference](#node-types-reference)
- [Error Handling](#error-handling)

---

## File Operations

### get_file()

Get complete file information including document tree, styles, and components.

**Endpoint**: `GET /api/v1/files/{file_key}`

**Parameters**:
- `file_key` (required, string): Figma file unique identifier
- `version` (optional, string): Specific version ID
- `depth` (optional, integer): Node depth limit (1-5)
- `geometry` (optional, boolean): Include absolute bounding box geometry

**Returns**: Dictionary with file structure
```python
{
    "name": str,              # File name
    "lastModified": str,      # ISO 8601 timestamp
    "version": str,           # Current version ID
    "thumbnailUrl": str,      # File thumbnail URL
    "document": {             # Document root node
        "id": str,
        "name": str,
        "type": "DOCUMENT",
        "children": [...]     # Page nodes
    },
    "components": {...},      # Component definitions
    "styles": {...},          # Style definitions
    "schemaVersion": int      # Schema version
}
```

**Python Example**:
```python
async with FigmaFileClient() as client:
    file_data = await client.get_file(
        file_key="abc123def456",
        depth=2,              # Limit tree depth
        geometry=True         # Include bounding boxes
    )

    # Access file metadata
    print(f"File: {file_data['name']}")
    print(f"Version: {file_data['version']}")
    print(f"Modified: {file_data['lastModified']}")

    # Access document structure
    for page in file_data['document']['children']:
        print(f"Page: {page['name']}")
```

**Bash Example**:
```bash
# Using the bundled script
python scripts/figma_file_client.py get-file \
  --file-key abc123def456 \
  --depth 2 \
  --geometry
```

---

### get_file_nodes()

Get specific nodes from a file with their properties and children.

**Endpoint**: `GET /api/v1/files/{file_key}/nodes`

**Parameters**:
- `file_key` (required, string): Figma file unique identifier
- `ids` (required, string): Comma-separated node IDs (e.g., "123:456,789:012")
- `version` (optional, string): Specific version ID
- `depth` (optional, integer): Node depth limit

**Returns**: Dictionary mapping node IDs to node data
```python
{
    "name": str,
    "lastModified": str,
    "thumbnailUrl": str,
    "version": str,
    "nodes": {
        "123:456": {
            "document": {         # Node data
                "id": str,
                "name": str,
                "type": str,      # Node type
                "children": [...],
                ...               # Node-specific properties
            },
            "components": {...},
            "styles": {...}
        },
        "789:012": {...}
    }
}
```

**Python Example**:
```python
async with FigmaFileClient() as client:
    nodes = await client.get_file_nodes(
        file_key="abc123def456",
        node_ids=["123:456", "789:012", "345:678"]
    )

    # Process each node
    for node_id, node_info in nodes['nodes'].items():
        node_doc = node_info['document']
        print(f"Node {node_id}: {node_doc['name']} ({node_doc['type']})")
```

**Bash Example**:
```bash
python scripts/figma_file_client.py get-nodes \
  --file-key abc123def456 \
  --node-ids "123:456,789:012"
```

---

### get_file_versions()

Get file version history with labels, timestamps, and authors.

**Endpoint**: `GET /api/v1/files/{file_key}/versions`

**Parameters**:
- `file_key` (required, string): Figma file unique identifier

**Returns**: Dictionary with version history
```python
{
    "versions": [
        {
            "id": str,             # Version ID
            "created_at": str,     # ISO 8601 timestamp
            "label": str,          # Version label/name
            "description": str,    # Version description
            "user": {              # User who created version
                "id": str,
                "handle": str,
                "img_url": str
            }
        },
        ...
    ],
    "pagination": {
        "next_page": str | null
    }
}
```

**Python Example**:
```python
async with FigmaFileClient() as client:
    versions = await client.get_file_versions(file_key="abc123def456")

    # Display version history
    for version in versions['versions']:
        print(f"Version: {version['label']}")
        print(f"  Created: {version['created_at']}")
        print(f"  By: {version['user']['handle']}")
        print(f"  Description: {version.get('description', 'N/A')}")
        print()
```

**Bash Example**:
```bash
python scripts/figma_file_client.py get-versions \
  --file-key abc123def456
```

---

## Node Operations

### traverse_nodes()

Recursively traverse node tree with callback function.

**Function Signature**:
```python
def traverse_nodes(
    node: Dict,
    callback: Callable[[Dict, int], None],
    level: int = 0
) -> None
```

**Parameters**:
- `node` (Dict): Starting node
- `callback` (Callable): Function to call for each node, receives (node, level)
- `level` (int): Starting depth level (default: 0)

**Example**:
```python
from scripts.traverse_nodes import traverse_nodes

async with FigmaFileClient() as client:
    file_data = await client.get_file(file_key="abc123def456")

    # Print tree structure
    def print_node(node, level):
        indent = "  " * level
        print(f"{indent}{node['name']} ({node.get('type', 'UNKNOWN')})")

    traverse_nodes(file_data['document'], print_node)
```

**Output**:
```
Document (DOCUMENT)
  Page 1 (CANVAS)
    Frame 1 (FRAME)
      Text Layer (TEXT)
      Rectangle (RECTANGLE)
  Page 2 (CANVAS)
    ...
```

---

### find_nodes_by_type()

Find all nodes matching a specific type.

**Function Signature**:
```python
def find_nodes_by_type(
    node: Dict,
    target_type: str,
    results: List[Dict] = None
) -> List[Dict]
```

**Parameters**:
- `node` (Dict): Starting node
- `target_type` (str): Node type to search for
- `results` (List[Dict]): Accumulator list (optional)

**Returns**: List of matching nodes

**Example**:
```python
from scripts.find_nodes import find_nodes_by_type

async with FigmaFileClient() as client:
    file_data = await client.get_file(file_key="abc123def456")

    # Find all FRAME nodes
    frames = find_nodes_by_type(file_data['document'], 'FRAME')
    print(f"Found {len(frames)} frames:")
    for frame in frames:
        print(f"  - {frame['name']} (ID: {frame['id']})")
```

---

### find_nodes_by_name()

Find nodes matching a name pattern (regex).

**Function Signature**:
```python
def find_nodes_by_name(
    node: Dict,
    pattern: str,
    results: List[Dict] = None,
    case_sensitive: bool = False
) -> List[Dict]
```

**Parameters**:
- `node` (Dict): Starting node
- `pattern` (str): Regex pattern to match against node names
- `results` (List[Dict]): Accumulator list (optional)
- `case_sensitive` (bool): Whether search is case sensitive

**Returns**: List of matching nodes

**Example**:
```python
from scripts.find_nodes import find_nodes_by_name

async with FigmaFileClient() as client:
    file_data = await client.get_file(file_key="abc123def456")

    # Find nodes containing "菜品" (dish)
    dish_nodes = find_nodes_by_name(file_data['document'], r'菜品')
    print(f"Found {len(dish_nodes)} dish nodes:")
    for node in dish_nodes:
        print(f"  - {node['name']} ({node['type']})")
```

---

## Node Types Reference

Common Figma node types and their properties:

### DOCUMENT
Root node of the file.
- **Properties**: `id`, `name`, `type`, `children`
- **Children**: CANVAS (pages)

### CANVAS
Top-level page in the document.
- **Properties**: `id`, `name`, `type`, `children`, `backgroundColor`
- **Children**: FRAME, GROUP, COMPONENT, etc.

### FRAME
Container frame, the most common layout element.
- **Properties**: `id`, `name`, `type`, `children`, `absoluteBoundingBox`, `backgroundColor`, `fills`, `effects`
- **Children**: Any node type

### GROUP
Group of nodes.
- **Properties**: `id`, `name`, `type`, `children`, `absoluteBoundingBox`
- **Children**: Any node type

### COMPONENT
Master component definition.
- **Properties**: `id`, `name`, `type`, `children`, `componentId`
- **Children**: Any node type

### INSTANCE
Instance of a component.
- **Properties**: `id`, `name`, `type`, `children`, `componentId`, `overrides`
- **Children**: Mirrors component structure

### TEXT
Text layer.
- **Properties**: `id`, `name`, `type`, `characters`, `style`, `fills`
- **No children**

### RECTANGLE / ELLIPSE / POLYGON / STAR / LINE / VECTOR
Shape nodes.
- **Properties**: `id`, `name`, `type`, `fills`, `strokes`, `effects`, `absoluteBoundingBox`
- **No children** (except VECTOR can have children)

### BOOLEAN_OPERATION
Boolean operation result (union, subtract, intersect, exclude).
- **Properties**: `id`, `name`, `type`, `children`, `booleanOperation`
- **Children**: Shape nodes

---

## Error Handling

### Error Types

```python
from scripts.figma_file_client import (
    FigmaAPIError,           # Base error
    FigmaAuthenticationError, # 401/403 errors
    FigmaNotFoundError,       # 404 errors
    FigmaRateLimitError      # 429 errors
)
```

### Error Handling Examples

**Basic try-catch**:
```python
from scripts.figma_file_client import FigmaFileClient, FigmaAPIError

async with FigmaFileClient() as client:
    try:
        file_data = await client.get_file(file_key="abc123")
    except FigmaAuthenticationError as e:
        print(f"Authentication failed: {e.message}")
        print("Check your FIGMA_API_TOKEN")
    except FigmaNotFoundError as e:
        print(f"File not found: {e.message}")
        print("Verify the file_key is correct")
    except FigmaRateLimitError as e:
        print(f"Rate limited: {e.message}")
        print("Wait and retry (automatic backoff enabled)")
    except FigmaAPIError as e:
        print(f"API error: {e.message}")
        print(f"Status code: {e.status_code}")
```

**Automatic retry with backoff**:
The client automatically retries on network errors and rate limits using exponential backoff:

```python
# Client configuration (defaults shown)
from scripts.figma_file_client import FigmaFileClient, FigmaClientConfig

config = FigmaClientConfig(
    figma_max_retries=3,           # Max retry attempts
    figma_timeout=30,              # Request timeout (seconds)
    figma_concurrent_requests=5    # Max concurrent requests
)

async with FigmaFileClient(config=config) as client:
    # Automatic retry on:
    # - httpx.RequestError (network issues)
    # - FigmaRateLimitError (429 responses)
    file_data = await client.get_file(file_key="abc123")
```

**Validate response data**:
```python
async with FigmaFileClient() as client:
    file_data = await client.get_file(file_key="abc123")

    # Check required fields exist
    if 'document' not in file_data:
        raise ValueError("Invalid response: missing 'document' field")

    # Validate document structure
    document = file_data['document']
    if document.get('type') != 'DOCUMENT':
        raise ValueError(f"Invalid root node type: {document.get('type')}")

    # Safe navigation with get()
    pages = document.get('children', [])
    if not pages:
        print("Warning: Document has no pages")
```

---

## Performance Optimization

### Batch node queries
Query multiple nodes in a single request:

```python
# Inefficient: Multiple requests
for node_id in node_ids:
    node = await client.get_file_nodes(file_key, [node_id])

# Efficient: Single batched request
nodes = await client.get_file_nodes(file_key, node_ids)
```

### Limit tree depth
For large files, limit depth to reduce response size:

```python
# Get only top-level structure
file_data = await client.get_file(file_key, depth=2)

# Then query specific nodes for details
detailed_nodes = await client.get_file_nodes(file_key, target_node_ids)
```

### Concurrent requests
Use semaphore to control concurrency (built into client):

```python
# Client automatically limits concurrent requests
# Default: 5 concurrent requests
# Configure via FigmaClientConfig

import asyncio

async def fetch_multiple_files(file_keys):
    async with FigmaFileClient() as client:
        tasks = [client.get_file(file_key) for file_key in file_keys]
        # Automatically throttled to max 5 concurrent
        results = await asyncio.gather(*tasks)
    return results
```

---

## Configuration

### Environment Variables

```bash
# Required
export FIGMA_API_TOKEN=your_personal_access_token

# Optional (with defaults)
export FIGMA_API_BASE_URL=https://api.figma.com/v1/
export FIGMA_TIMEOUT=30
export FIGMA_MAX_RETRIES=3
export FIGMA_RATE_LIMIT_PER_MINUTE=60
export FIGMA_CONCURRENT_REQUESTS=5
```

### Configuration Object

```python
from scripts.figma_file_client import FigmaClientConfig

config = FigmaClientConfig(
    figma_api_token="your_token",
    figma_api_base_url="https://api.figma.com/v1/",
    figma_timeout=30,
    figma_max_retries=3,
    figma_rate_limit_per_minute=60,
    figma_concurrent_requests=5
)

async with FigmaFileClient(config=config) as client:
    # Use client with custom config
    ...
```

---

## Rate Limiting

Figma API rate limits (as of 2024):
- **500 requests per minute** per access token
- **Rate limit headers** included in responses

The client handles rate limiting automatically:
1. Tracks requests per minute
2. Implements exponential backoff on 429 errors
3. Retries up to `max_retries` times

**Monitor rate limits**:
```python
# Response headers include rate limit info
# X-RateLimit-Limit: 500
# X-RateLimit-Remaining: 450
# X-RateLimit-Reset: 1640000000

# Client automatically respects these headers
```

---

## Advanced Usage

### Caching file data
```python
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=128)
async def get_file_cached(file_key, ttl_minutes=60):
    cache_time = datetime.now()

    async with FigmaFileClient() as client:
        file_data = await client.get_file(file_key)

    return {
        'data': file_data,
        'cached_at': cache_time,
        'expires_at': cache_time + timedelta(minutes=ttl_minutes)
    }
```

### Incremental loading
```python
async def load_file_incrementally(file_key):
    async with FigmaFileClient() as client:
        # 1. Get top-level structure only
        file_data = await client.get_file(file_key, depth=1)

        # 2. Identify frames of interest
        frames = find_nodes_by_type(file_data['document'], 'FRAME')
        target_frame_ids = [f['id'] for f in frames[:10]]  # First 10

        # 3. Load detailed frame data
        detailed_frames = await client.get_file_nodes(
            file_key,
            target_frame_ids
        )

    return detailed_frames
```

---

For more examples, see [examples.md](examples.md).
