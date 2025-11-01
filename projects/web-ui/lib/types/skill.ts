/**
 * Skill Type Definitions
 */

export interface Skill {
  id: string;
  name: string;
  description: string;
  category: string;
  categoryPath: string;
  filePath: string;
  version?: string;
  tools: string[];
  tags: string[];
  capabilities: string[];
}

export interface SkillsData {
  version: string;
  generatedAt: string;
  totalSkills: number;
  categories: string[];
  skills: Skill[];
}
