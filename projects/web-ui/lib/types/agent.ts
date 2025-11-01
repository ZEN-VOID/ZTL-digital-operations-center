/**
 * Agent type definitions
 */

export interface McpServer {
  name: string;
  tools: string[];
}

export interface Skill {
  name: string;
  description: string;
  category?: string;
  version?: string;
}

export interface AgentRelationship {
  agentId: string;
  agentName: string;
  relationshipType: 'orchestrates' | 'delegates' | 'reports-to' | 'collaborates-with';
  description?: string;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  group: string;
  groupPath?: string;
  filePath?: string;
  expertise?: string[];
  tools?: string[] | string;
  model?: string;
  status?: 'online' | 'offline' | 'busy' | 'idle';
  mcpServers?: McpServer[];
  skills?: Skill[];
  workflows?: string[];
  outputPath?: string;
  color?: string;
  upstream?: AgentRelationship[];
  downstream?: AgentRelationship[];
}

export interface AgentsIndex {
  version: string;
  generatedAt: string;
  totalAgents: number;
  groups: string[];
  agents: Agent[];
}
