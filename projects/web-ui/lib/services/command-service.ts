/**
 * Command Service
 * Provides metadata for commands from .claude/commands directory
 */

export interface CommandMetadata {
  name: string;
  description: string;
  version?: string;
  shortcut: string;
  category?: string;
}

/**
 * Static command metadata extracted from .claude/commands/*.md files
 * Note: This data is synchronized from the actual command files
 */
const COMMAND_DATA: CommandMetadata[] = [
  {
    name: '测试与质量验证工程师',
    description: '全面测试与质量验证,确保代码变更通过严格验证并符合质量标准',
    version: '3.0.0',
    shortcut: '/test',
    category: '开发工具',
  },
  {
    name: 'GitHub同步推送',
    description: '将本地项目完整同步推送到GitHub仓库,确保远程与本地完全一致',
    version: '7.0.0',
    shortcut: '/github-pull',
    category: 'Git工具',
  },
  {
    name: 'GitHub仓库初始化',
    description: '自动化GitHub仓库创建、初始化和首次推送流程',
    shortcut: '/github-start',
    category: 'Git工具',
  },
  {
    name: 'GitHub Issue处理',
    description: '系统化的Issue分析、修复和关闭流程,确保问题解决的完整性和可追溯性',
    shortcut: '/github-issue',
    category: 'Git工具',
  },
  {
    name: 'Context-Aware Analysis',
    description: '全面分析项目8大维度的上下文:智能体、命令、钩子、技能包、项目结构、知识积累、配置文件、文档说明',
    version: '3.0.0',
    shortcut: '/context-aware',
    category: '项目分析',
  },
  {
    name: 'Plan-Research-Plan',
    description: '快速生成功能规划文档(Plan-Research-Plan),专注研究和规划阶段',
    shortcut: '/prp',
    category: '项目规划',
  },
  {
    name: '并行执行工作流',
    description: '完整的并行执行工作流:环境准备 → 并行执行,实现多方案探索',
    shortcut: '/trees',
    category: '工作流',
  },
  {
    name: '清理并行工作树',
    description: '彻底清理 /trees 命令产生的所有工作树、分支和目录残留',
    shortcut: '/trees-clean',
    category: '工作流',
  },
  {
    name: '跨工作区同步',
    description: '基于相对路径的新增或覆盖操作,自动识别并批量同步到所有关联工作区',
    shortcut: '/links',
    category: '工作流',
  },
  {
    name: '插件生态研究',
    description: 'Plugin健康度分析、协作关系图、演进计划生成',
    shortcut: '/learn',
    category: '项目分析',
  },
  {
    name: 'README文档生成',
    description: '自动更新项目根目录和所有子目录的README文档',
    shortcut: '/readme-generator',
    category: '文档工具',
  },
  {
    name: '项目说明文档管理',
    description: '全面管理project/instructions目录下的完整文档体系',
    shortcut: '/project-instructions',
    category: '文档工具',
  },
];

/**
 * Get all available commands
 */
export function getAllCommands(): CommandMetadata[] {
  return [...COMMAND_DATA];
}

/**
 * Get command metadata by shortcut
 */
export function getCommandByShortcut(commands: CommandMetadata[], shortcut: string): CommandMetadata | undefined {
  return commands.find((cmd) => cmd.shortcut === shortcut);
}

/**
 * Filter commands by search query
 */
export function filterCommands(commands: CommandMetadata[], query: string): CommandMetadata[] {
  if (!query) return commands;

  const lowerQuery = query.toLowerCase();
  return commands.filter(
    (cmd) =>
      cmd.name.toLowerCase().includes(lowerQuery) ||
      cmd.description.toLowerCase().includes(lowerQuery) ||
      cmd.shortcut?.toLowerCase().includes(lowerQuery)
  );
}
