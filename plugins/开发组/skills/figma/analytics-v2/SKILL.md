---
name: Figma Analytics
description: Analyze Figma files for structure, quality, component usage, and design patterns. Use when auditing designs, assessing quality, discovering reusable patterns, or when user mentions design analysis, quality check, or component audit. Requires Figma API token.
---

# Figma Analytics

## Quick Start

### Analyze file structure
```python
import sys
sys.path.append('./plugins/创意组/skills/figma/analytics-v2/scripts')
from analytics_client import AnalyticsClient

async with AnalyticsClient() as client:
    analysis = await client.analyze_file_structure(file_key="YOUR_FILE_KEY")
    print(f"Pages: {analysis['page_count']}")
    print(f"Frames: {analysis['frame_count']}")
    print(f"Max depth: {analysis['max_depth']}")
```

### Assess design quality
```bash
python scripts/quality_assessment.py --file-key YOUR_FILE_KEY
```

## Documentation

- **[API Reference](reference.md)**: Complete analytics API documentation
- **[Quality Metrics](quality-metrics.md)**: Design quality assessment criteria
- **[Examples](examples.md)**: Analysis examples and reports

## Bundled Scripts

- **`scripts/analytics_client.py`**: Core analytics operations
- **`scripts/quality_assessment.py`**: Design quality evaluation
- **`scripts/component_audit.py`**: Component usage analysis
- **`scripts/pattern_discovery.py`**: Find reusable design patterns

## Requirements

```bash
pip install httpx backoff pydantic-settings
export FIGMA_API_TOKEN=your_token_here
```

## Related Skills

- For file operations: See `../file-management-v2/SKILL.md`
- For design system: See `../design-system-v2/SKILL.md`
