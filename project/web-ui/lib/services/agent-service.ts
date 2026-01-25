/**
 * Agent Service
 * Handles loading and filtering of agent data
 */

import type { Agent, AgentsIndex } from '@/lib/types/agent';

/**
 * Load agents index from JSON file
 */
export async function loadAgentsIndex(): Promise<AgentsIndex> {
  try {
    const response = await fetch('/data/agents-index.json');
    if (!response.ok) {
      throw new Error(`Failed to load agents index: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error loading agents index:', error);
    throw error;
  }
}

/**
 * Get all agents
 */
export async function getAllAgents(): Promise<Agent[]> {
  const index = await loadAgentsIndex();
  return index.agents;
}

/**
 * Get all groups
 */
export async function getAllGroups(): Promise<string[]> {
  const index = await loadAgentsIndex();
  return index.groups;
}

/**
 * Filter agents by group
 */
export function filterAgentsByGroup(agents: Agent[], group: string | null): Agent[] {
  if (!group || group === 'all') {
    return agents;
  }
  return agents.filter((agent) => agent.group === group);
}

/**
 * Search agents by name or description
 */
export function searchAgents(agents: Agent[], query: string): Agent[] {
  if (!query.trim()) {
    return agents;
  }

  const lowerQuery = query.toLowerCase();
  return agents.filter(
    (agent) =>
      agent.name.toLowerCase().includes(lowerQuery) ||
      agent.description.toLowerCase().includes(lowerQuery) ||
      agent.id.toLowerCase().includes(lowerQuery)
  );
}

/**
 * Get agent by ID
 */
export function getAgentById(agents: Agent[], id: string): Agent | undefined {
  return agents.find((agent) => agent.id === id);
}

/**
 * Normalize tools to array
 */
export function normalizeTools(tools?: string[] | string): string[] {
  if (!tools) return [];
  if (Array.isArray(tools)) return tools;
  return tools.split(',').map((t) => t.trim()).filter(Boolean);
}
