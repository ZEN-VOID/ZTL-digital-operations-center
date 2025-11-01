/**
 * Agent Parser Script
 * Scans plugins directory agents files and generates agents-index.json
 */

import { readFileSync, writeFileSync, readdirSync, statSync, mkdirSync, existsSync } from 'fs';
import { join, basename, dirname } from 'path';
import * as yaml from 'yaml';

interface McpServer {
  name: string;
  tools: string[];
}

interface Skill {
  name: string;
  description: string;
  category?: string;
  version?: string;
}

interface AgentMetadata {
  id: string;
  name: string;
  description: string;
  group: string;
  groupPath: string;
  filePath: string;
  expertise?: string[];
  tools?: string[];
  model?: string;
  workflows?: string[];
  outputPath?: string;
  mcpServers?: McpServer[];
  skills?: Skill[];
  color?: string;
}

interface AgentIndex {
  version: string;
  generatedAt: string;
  totalAgents: number;
  groups: string[];
  agents: AgentMetadata[];
}


function parseYamlFrontmatter(content: string): Record<string, any> | null {
  const frontmatterRegex = /^---\n([\s\S]*?)\n---/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    return null;
  }

  try {
    const parsed = yaml.parse(match[1]);

    // Normalize tools to array if it's a string
    if (parsed && parsed.tools) {
      if (typeof parsed.tools === 'string') {
        parsed.tools = [parsed.tools];
      } else if (!Array.isArray(parsed.tools)) {
        parsed.tools = Object.values(parsed.tools).filter(v => v);
      }
    }

    return parsed;
  } catch (error) {
    // Try alternative parsing: extract name and description manually
    const yamlContent = match[1];
    const nameMatch = yamlContent.match(/^name:\s*(.+)$/m);
    const descMatch = yamlContent.match(/^description:\s*(.+)$/m);
    const modelMatch = yamlContent.match(/^model:\s*(.+)$/m);

    // Try to extract tools from multi-line YAML array
    let tools: string[] | undefined = undefined;
    const toolsMatch = yamlContent.match(/^tools:\s*\[(.+)\]$/m);
    if (toolsMatch) {
      tools = toolsMatch[1].split(',').map((t: string) => t.trim().replace(/['"]/g, ''));
    } else {
      // Try multi-line array format
      const toolsSection = yamlContent.match(/^tools:\s*\n((?:\s+-\s+.+\n?)+)/m);
      if (toolsSection) {
        tools = toolsSection[1]
          .split('\n')
          .filter((line: string) => line.trim().startsWith('-'))
          .map((line: string) => line.replace(/^\s*-\s*/, '').trim())
          .filter((tool: string) => tool.length > 0);
      }
    }

    if (nameMatch || descMatch) {
      return {
        name: nameMatch ? nameMatch[1].trim() : undefined,
        description: descMatch ? descMatch[1].trim().replace(/\\n/g, ' ') : undefined,
        model: modelMatch ? modelMatch[1].trim() : undefined,
        tools: tools,
      };
    }

    console.warn('Failed to parse YAML frontmatter, no fallback available');
    return null;
  }
}

function parseAgentFile(filePath: string, groupName: string, groupPath: string): AgentMetadata | null {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const frontmatter = parseYamlFrontmatter(content);

    if (!frontmatter) {
      console.warn(`No YAML frontmatter found in: ${filePath}`);
      return null;
    }

    const fileName = basename(filePath, '.md');

    // Extract English ID and Chinese name from filename pattern: [PREFIX]-[CHINESE_NAME]
    // e.g., "GG-战略组组长" → id="GG", name="战略组组长"
    const fileNameMatch = fileName.match(/^([A-Z]+\d*)-(.+)$/);
    let agentId: string;
    let agentName: string;

    if (fileNameMatch) {
      agentId = fileNameMatch[1]; // English prefix (e.g., "GG", "G1", "CC")
      agentName = fileNameMatch[2]; // Chinese name (e.g., "战略组组长")
    } else {
      // Fallback: use full filename if pattern doesn't match
      agentId = fileName;
      agentName = frontmatter.name || fileName;
    }

    const workflowRegex = /## (?:工作流程|Workflow|核心流程)([\s\S]*?)(?=##|$)/gi;
    const workflowMatches = content.matchAll(workflowRegex);
    const workflows: string[] = [];

    for (const match of workflowMatches) {
      const workflowContent = match[1].trim();
      const steps = workflowContent
        .split('\n')
        .filter((line: string) => line.match(/^[\d\-\*]\s+/))
        .map((line: string) => line.replace(/^[\d\-\*]\s+/, '').trim());
      workflows.push(...steps);
    }

    // Extract MCP servers from tools array
    const mcpServers: McpServer[] = [];
    if (frontmatter.tools) {
      const tools = Array.isArray(frontmatter.tools) ? frontmatter.tools : [frontmatter.tools];
      tools.forEach((tool: string) => {
        const mcpMatch = tool.match(/^mcp__(.+?)__/);
        if (mcpMatch) {
          const serverName = mcpMatch[1];
          const existing = mcpServers.find((s: McpServer) => s.name === serverName);
          if (existing) {
            existing.tools.push(tool);
          } else {
            mcpServers.push({ name: serverName, tools: [tool] });
          }
        }
      });
    }

    // Extract skills from content (look for Skill() calls)
    const skills: Skill[] = [];
    const skillRegex = /Skill\(['"]([^'"]+)['"]\)/g;
    const skillMatches = content.matchAll(skillRegex);
    for (const match of skillMatches) {
      const skillName = match[1];
      // Try to find skill metadata from .claude/skills directory
      const skillPath = join(process.cwd(), '..', '..', '.claude', 'skills', skillName);
      if (existsSync(skillPath)) {
        const skillMdPath = join(skillPath, 'SKILL.md');
        if (existsSync(skillMdPath)) {
          try {
            const skillContent = readFileSync(skillMdPath, 'utf-8');
            const skillFrontmatter = parseYamlFrontmatter(skillContent);
            if (skillFrontmatter) {
              skills.push({
                name: skillFrontmatter.name || skillName,
                description: skillFrontmatter.description || '',
                category: dirname(skillPath).split('/').pop(),
                version: skillFrontmatter.version,
              });
            }
          } catch {
            // If skill parsing fails, just add the name
            skills.push({ name: skillName, description: '' });
          }
        }
      }
    }

    return {
      id: agentId,
      name: agentName,
      description: frontmatter.description || '',
      group: groupName,
      groupPath: groupPath,
      filePath: filePath.replace(process.cwd(), ''),
      expertise: frontmatter.expertise || [],
      tools: frontmatter.tools || [],
      model: frontmatter.model,
      workflows: workflows.length > 0 ? workflows : undefined,
      outputPath: frontmatter.outputPath,
      mcpServers: mcpServers.length > 0 ? mcpServers : undefined,
      skills: skills.length > 0 ? skills : undefined,
      color: frontmatter.color,
    };
  } catch (error) {
    console.error(`Failed to parse agent file: ${filePath}`, error);
    return null;
  }
}

function scanAgentFiles(pluginsDir: string): AgentMetadata[] {
  const agents: AgentMetadata[] = [];

  try {
    const groupDirs = readdirSync(pluginsDir);

    for (const groupDir of groupDirs) {
      const groupPath = join(pluginsDir, groupDir);
      const stat = statSync(groupPath);

      if (!stat.isDirectory()) {
        continue;
      }

      const agentsDir = join(groupPath, 'agents');

      if (!existsSync(agentsDir)) {
        continue;
      }

      const agentFiles = readdirSync(agentsDir).filter((file: string) => file.endsWith('.md'));

      for (const agentFile of agentFiles) {
        const agentPath = join(agentsDir, agentFile);
        const agentMetadata = parseAgentFile(agentPath, groupDir, groupPath);

        if (agentMetadata) {
          agents.push(agentMetadata);
        }
      }
    }
  } catch (error) {
    console.error('Failed to scan agent files:', error);
  }

  return agents;
}

function scanCommandCenterAgents(claudeAgentsDir: string): AgentMetadata[] {
  const agents: AgentMetadata[] = [];

  try {
    if (!existsSync(claudeAgentsDir)) {
      console.log(`⚠️  Command center directory not found: ${claudeAgentsDir}`);
      return agents;
    }

    const agentFiles = readdirSync(claudeAgentsDir).filter((file: string) => file.endsWith('.md'));

    for (const agentFile of agentFiles) {
      const agentPath = join(claudeAgentsDir, agentFile);
      const agentMetadata = parseAgentFile(agentPath, '指挥部', claudeAgentsDir);

      if (agentMetadata) {
        agents.push(agentMetadata);
      }
    }

    console.log(`✅ Found ${agents.length} command center agents`);
  } catch (error) {
    console.error('Failed to scan command center agents:', error);
  }

  return agents;
}

function generateAgentsIndex(): void {
  const rootDir = process.cwd();
  // Point to project root (two levels up from web-ui)
  const projectRootDir = join(rootDir, '..', '..');
  const pluginsDir = join(projectRootDir, 'plugins');
  const claudeAgentsDir = join(projectRootDir, '.claude', 'agents');
  const outputDir = join(rootDir, 'public', 'data');
  const outputFile = join(outputDir, 'agents-index.json');

  console.log('🔍 Scanning plugins directory:', pluginsDir);
  const pluginAgents = scanAgentFiles(pluginsDir);
  console.log(`✅ Found ${pluginAgents.length} plugin agents`);

  console.log('🔍 Scanning command center directory:', claudeAgentsDir);
  const commandCenterAgents = scanCommandCenterAgents(claudeAgentsDir);

  const agents = [...pluginAgents, ...commandCenterAgents];

  console.log(`✅ Total agents: ${agents.length}`);

  const groups = [...new Set(agents.map((agent: AgentMetadata) => agent.group))].sort();

  const index: AgentIndex = {
    version: '1.0.0',
    generatedAt: new Date().toISOString(),
    totalAgents: agents.length,
    groups: groups,
    agents: agents.sort((a: AgentMetadata, b: AgentMetadata) => a.id.localeCompare(b.id)),
  };

  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  writeFileSync(outputFile, JSON.stringify(index, null, 2), 'utf-8');

  console.log('📝 Generated agents index:', outputFile);
  console.log(`   - Total agents: ${index.totalAgents}`);
  console.log(`   - Groups: ${groups.join(', ')}`);

  console.log('\n📊 Agents by Group:');
  for (const group of groups) {
    const groupAgents = agents.filter((agent: AgentMetadata) => agent.group === group);
    console.log(`   - ${group}: ${groupAgents.length} agents`);
  }
}

if (require.main === module) {
  try {
    generateAgentsIndex();
    console.log('\n✨ Agent parsing completed successfully!');
  } catch (error) {
    console.error('\n❌ Agent parsing failed:', error);
    process.exit(1);
  }
}

export { parseAgentFile, scanAgentFiles, generateAgentsIndex };
export type { AgentMetadata, AgentIndex };
