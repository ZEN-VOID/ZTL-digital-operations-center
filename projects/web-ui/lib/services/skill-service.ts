/**
 * Skill Service
 * Provides methods to interact with skills data from skills.json
 */

import type { Skill, SkillsData } from '@/lib/types/skill';

/**
 * Load skills data from JSON file
 */
export async function loadSkillsData(): Promise<SkillsData> {
  try {
    const response = await fetch('/data/skills.json');
    if (!response.ok) {
      throw new Error(`Failed to fetch skills data: ${response.statusText}`);
    }
    const data: SkillsData = await response.json();
    return data;
  } catch (error) {
    console.error('Error loading skills data:', error);
    throw error;
  }
}

/**
 * Get all skills
 */
export async function getAllSkills(): Promise<Skill[]> {
  const data = await loadSkillsData();
  return data.skills;
}

/**
 * Get skill by ID
 */
export function getSkillById(skills: Skill[], id: string): Skill | undefined {
  return skills.find((skill) => skill.id === id);
}

/**
 * Filter skills by category
 */
export function filterSkillsByCategory(skills: Skill[], category: string | null): Skill[] {
  if (!category) return skills;
  return skills.filter((skill) => skill.category === category);
}

/**
 * Search skills by query
 * Searches in name, description, tags, and capabilities
 */
export function searchSkills(skills: Skill[], query: string): Skill[] {
  if (!query) return skills;

  const lowerQuery = query.toLowerCase();
  return skills.filter(
    (skill) =>
      skill.name.toLowerCase().includes(lowerQuery) ||
      skill.description.toLowerCase().includes(lowerQuery) ||
      skill.tags.some((tag) => tag.toLowerCase().includes(lowerQuery)) ||
      skill.capabilities.some((cap) => cap.toLowerCase().includes(lowerQuery))
  );
}

/**
 * Get unique categories from skills
 */
export function getCategories(skills: Skill[]): string[] {
  const categories = new Set(skills.map((skill) => skill.category));
  return Array.from(categories).sort();
}

/**
 * Get skills count per category
 */
export function getSkillsCountByCategory(skills: Skill[]): Record<string, number> {
  const counts: Record<string, number> = {};
  skills.forEach((skill) => {
    counts[skill.category] = (counts[skill.category] || 0) + 1;
  });
  return counts;
}

/**
 * Normalize tools array (similar to agent-service)
 */
export function normalizeTools(tools: string[] | undefined): string[] {
  if (!tools || !Array.isArray(tools)) return [];
  return tools;
}
