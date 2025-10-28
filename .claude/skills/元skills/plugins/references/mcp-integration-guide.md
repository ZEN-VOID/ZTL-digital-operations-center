# MCP Server Integration Guide

Complete guide for integrating Model Context Protocol (MCP) servers into Claude Code plugins.

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI systems to external tools and data sources.

**Key Concepts**:
- **Servers**: Processes that expose tools and resources
- **Clients**: AI systems (like Claude Code) that use these tools
- **Tools**: Functions the AI can call
- **Resources**: Data sources the AI can read
- **Prompts**: Pre-configured prompts servers can provide

## MCP Configuration in Plugins

### Configuration File

Create `.mcp.json` at plugin root:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

### Server Configuration Schema

```typescript
{
  "mcpServers": {
    "[server-name]": {
      // Connection type (required)
      "type": "stdio" | "sse" | "websocket",

      // Command to launch server (required)
      "command": "string",

      // Command arguments (optional)
      "args": ["string", ...],

      // Environment variables (optional)
      "env": {
        "KEY": "value"
      }
    }
  }
}
```

## Connection Types

### 1. STDIO (Standard Input/Output)

Most common type for local servers.

```json
{
  "type": "stdio",
  "command": "node",
  "args": ["server.js"]
}
```

**When to use**:
- Local servers
- Simple request/response patterns
- No need for bidirectional streaming

**Examples**:
```json
// Node.js server
{
  "type": "stdio",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/mcp-server.js"]
}

// Python server
{
  "type": "stdio",
  "command": "python3",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/mcp-server.py"]
}

// Go binary
{
  "type": "stdio",
  "command": "${CLAUDE_PLUGIN_ROOT}/bin/mcp-server"
}
```

### 2. SSE (Server-Sent Events)

For remote HTTP servers with streaming.

```json
{
  "type": "sse",
  "url": "https://api.example.com/mcp"
}
```

**When to use**:
- Remote services
- Streaming responses
- Cloud-hosted servers

### 3. WebSocket

For bidirectional real-time communication.

```json
{
  "type": "websocket",
  "url": "wss://api.example.com/mcp"
}
```

**When to use**:
- Real-time updates
- Bidirectional streaming
- Interactive services

## Environment Variables

### Using Plugin Root Path

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths:

```json
{
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/server.js"],
  "env": {
    "DATA_DIR": "${CLAUDE_PLUGIN_ROOT}/data",
    "CONFIG": "${CLAUDE_PLUGIN_ROOT}/config.json"
  }
}
```

**Available Variables**:
- `${CLAUDE_PLUGIN_ROOT}`: Plugin installation directory
- `${HOME}`: User home directory
- `${CWD}`: Current working directory

### Sensitive Data

**Do not hardcode secrets in .mcp.json!**

❌ Bad:
```json
{
  "env": {
    "API_KEY": "sk-1234567890abcdef"
  }
}
```

✅ Good:
```json
{
  "env": {
    "API_KEY": "${SECURITY_API_KEY}"
  }
}
```

**Setup Instructions**:
```bash
# Add to ~/.zshrc or ~/.bashrc
export SECURITY_API_KEY="sk-1234567890abcdef"

# Or use .env file (with dotenv)
echo "SECURITY_API_KEY=sk-1234567890abcdef" >> .env
```

## Complete Examples

### Example 1: Security Scanner

```json
{
  "mcpServers": {
    "security-scanner": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/security-mcp.js"],
      "env": {
        "SCAN_API_KEY": "${SECURITY_SCAN_API_KEY}",
        "LOG_LEVEL": "info",
        "SCAN_TIMEOUT": "30000"
      }
    }
  }
}
```

**Server Implementation** (`scripts/security-mcp.js`):
```javascript
#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'security-scanner',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {},
  },
});

// Define tools
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'scan_vulnerabilities',
      description: 'Scan code for security vulnerabilities',
      inputSchema: {
        type: 'object',
        properties: {
          path: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high'] }
        }
      }
    }
  ]
}));

// Implement tool
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'scan_vulnerabilities') {
    const { path, severity } = request.params.arguments;

    // Perform security scan
    const results = await performSecurityScan(path, severity);

    return {
      content: [
        { type: 'text', text: JSON.stringify(results, null, 2) }
      ]
    };
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Example 2: Database Query Tool

```json
{
  "mcpServers": {
    "postgres-client": {
      "type": "stdio",
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/postgres-mcp.py"],
      "env": {
        "DB_HOST": "${POSTGRES_HOST}",
        "DB_PORT": "${POSTGRES_PORT}",
        "DB_NAME": "${POSTGRES_DB}",
        "DB_USER": "${POSTGRES_USER}",
        "DB_PASSWORD": "${POSTGRES_PASSWORD}"
      }
    }
  }
}
```

**Server Implementation** (`scripts/postgres-mcp.py`):
```python
#!/usr/bin/env python3
import os
import json
import sys
import psycopg2
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Initialize server
server = Server("postgres-client")

# Database connection
db_config = {
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}

@server.list_tools()
async def list_tools():
    return [
        {
            "name": "query_database",
            "description": "Execute SQL query on database",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "query_database":
        query = arguments["query"]

        # Execute query
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()

        return {
            "content": [
                {"type": "text", "text": json.dumps(results)}
            ]
        }

# Run server
if __name__ == "__main__":
    stdio_server(server)
```

### Example 3: Remote API Service

```json
{
  "mcpServers": {
    "weather-api": {
      "type": "sse",
      "url": "https://api.weather.com/mcp",
      "env": {
        "API_KEY": "${WEATHER_API_KEY}"
      }
    }
  }
}
```

### Example 4: Real-Time Monitoring

```json
{
  "mcpServers": {
    "metrics-monitor": {
      "type": "websocket",
      "url": "wss://metrics.company.com/mcp",
      "env": {
        "AUTH_TOKEN": "${METRICS_AUTH_TOKEN}"
      }
    }
  }
}
```

## Multiple MCP Servers

Plugins can include multiple MCP servers:

```json
{
  "mcpServers": {
    "security-scanner": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/security-mcp.js"]
    },
    "performance-analyzer": {
      "type": "stdio",
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/performance-mcp.py"]
    },
    "deployment-manager": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/deploy-mcp"
    },
    "cloud-api": {
      "type": "sse",
      "url": "https://api.company.com/mcp",
      "env": {
        "API_KEY": "${CLOUD_API_KEY}"
      }
    }
  }
}
```

## Custom Paths

Override default .mcp.json location in plugin.json:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "mcpServers": "./config/mcp-servers.json"
}
```

## Best Practices

### 1. Use Portable Paths

Always use `${CLAUDE_PLUGIN_ROOT}`:

```json
✅ "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/server.js"]
❌ "args": ["/absolute/path/server.js"]
```

### 2. Externalize Secrets

Never commit secrets:

```json
✅ "API_KEY": "${SECURITY_API_KEY}"
❌ "API_KEY": "sk-1234567890"
```

### 3. Provide Setup Instructions

Document required environment variables:

```markdown
## Setup

Set required environment variables:

```bash
export SECURITY_API_KEY="your-key-here"
export DB_PASSWORD="your-password-here"
```
```

### 4. Handle Errors Gracefully

Server should handle errors and return proper responses:

```javascript
server.setRequestHandler('tools/call', async (request) => {
  try {
    // Tool logic
    return { content: [...] };
  } catch (error) {
    return {
      content: [
        { type: 'text', text: `Error: ${error.message}` }
      ],
      isError: true
    };
  }
});
```

### 5. Log for Debugging

Add logging to help with troubleshooting:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name} with {arguments}")
    # Tool logic
```

### 6. Test Independently

Test MCP servers separately:

```bash
# Test Node.js server
echo '{"method":"tools/list"}' | node scripts/security-mcp.js

# Test Python server
echo '{"method":"tools/list"}' | python3 scripts/postgres-mcp.py
```

## Debugging

### Server Not Starting

**Check**:
1. Command exists and is executable
2. Script paths are correct
3. Environment variables are set
4. Script has proper shebang line

**Debug**:
```bash
# Test command directly
node ${CLAUDE_PLUGIN_ROOT}/scripts/server.js

# Check environment
env | grep API_KEY

# Run with debug output
claude --debug
```

### Tools Not Available

**Check**:
1. Server connected successfully
2. Tools registered properly
3. Tool names match in calls
4. Input schema valid

**Debug**:
```bash
# List available tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node server.js
```

### Authentication Errors

**Check**:
1. API keys set in environment
2. Environment variables referenced correctly
3. Keys have proper permissions
4. Keys not expired

## Testing

### Unit Testing MCP Servers

```javascript
// test/security-mcp.test.js
import { expect } from 'chai';
import { Server } from '../scripts/security-mcp.js';

describe('Security MCP Server', () => {
  let server;

  beforeEach(() => {
    server = new Server();
  });

  it('should list tools', async () => {
    const tools = await server.listTools();
    expect(tools).to.have.lengthOf(1);
    expect(tools[0].name).to.equal('scan_vulnerabilities');
  });

  it('should scan for vulnerabilities', async () => {
    const result = await server.callTool('scan_vulnerabilities', {
      path: './test-code.js',
      severity: 'high'
    });
    expect(result.content).to.be.an('array');
  });
});
```

### Integration Testing

```bash
#!/bin/bash
# test/integration-test.sh

# Start server in background
node scripts/security-mcp.js &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Test tool list
echo '{"method":"tools/list"}' | nc localhost 3000

# Test tool call
echo '{"method":"tools/call","params":{"name":"scan_vulnerabilities","arguments":{"path":"./test.js"}}}' | nc localhost 3000

# Cleanup
kill $SERVER_PID
```

## Security Considerations

1. **Validate Input**: Always validate and sanitize tool inputs
2. **Least Privilege**: Only request necessary permissions
3. **Secure Communication**: Use HTTPS/WSS for remote servers
4. **Rate Limiting**: Implement rate limits on tool calls
5. **Audit Logging**: Log all tool invocations
6. **Error Handling**: Don't expose sensitive info in errors

## Performance Optimization

1. **Connection Pooling**: Reuse database connections
2. **Caching**: Cache frequently accessed data
3. **Async Operations**: Use async/await for I/O
4. **Batching**: Support batch operations when possible
5. **Timeouts**: Set reasonable timeouts
6. **Resource Limits**: Limit memory and CPU usage

## References

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP SDK (Node.js)](https://github.com/modelcontextprotocol/sdk-node)
- [MCP SDK (Python)](https://github.com/modelcontextprotocol/sdk-python)
- [Claude Code MCP Guide](https://docs.claude.com/zh-CN/docs/claude-code/mcp)
