#!/bin/bash
# Update Q series agents in .claude/agents

BASE_DIR="/Users/vincentlee/Desktop/ZTL数智化作战中心/.claude/agents"

update_agent() {
  local agent_id="$1"
  local new_desc="$2"
  local file="$BASE_DIR/${agent_id}.md"

  if [ ! -f "$file" ]; then
    echo "❌ ${agent_id}: File not found"
    return 1
  fi

  temp_file=$(mktemp)

  awk -v new_desc="$new_desc" '
    BEGIN { in_frontmatter = 0; after_description = 0; skip_lines = 0 }
    /^---$/ {
      if (NR == 1) { in_frontmatter = 1 }
      else if (in_frontmatter) { in_frontmatter = 0 }
      print
      next
    }
    in_frontmatter && /^description:/ {
      print "description: " new_desc
      skip_lines = 1
      after_description = 1
      next
    }
    after_description && skip_lines && /^$/ {
      skip_lines = 0
      print
      next
    }
    after_description && skip_lines && /^[a-zA-Z_-]+:/ {
      skip_lines = 0
      print
      next
    }
    skip_lines { next }
    { print }
  ' "$file" > "$temp_file"

  if [ -s "$temp_file" ]; then
    mv "$temp_file" "$file"
    echo "✅ ${agent_id}: Updated"
    return 0
  else
    rm "$temp_file"
    echo "❌ ${agent_id}: Failed"
    return 1
  fi
}

update_agent "Q2-技术文档专员" "技术文档专员,技术写作和内容创作专家。主动用于用户指南、教程、README文件、架构文档,提升内容清晰度和可访问性。适用于文档编写、技术传播等场景。"
update_agent "Q3-变更日志专员" "变更日志专员,变更日志和发布说明专家。主动用于从git历史生成变更日志、创建发布说明、维护版本文档。适用于版本管理、发布流程等场景。"
update_agent "Q5-上下文协调官" "上下文协调官,多智能体工作流和长时任务的上下文管理专家。主动用于复杂项目、会话协调、需要跨多个智能体保持上下文连续性的场景。"
update_agent "Q6-项目流程协调官" "项目流程协调官,项目工作流编排器。主动用于管理复杂的多步骤工作流,协调多个专业智能体按序工作,进行智能路由和负载验证。适用于复杂项目管理、流程自动化等场景。"
update_agent "Q7-运维监控协调官" "运维监控协调官,监控和可观测性基础设施专家。主动用于指标收集、告警系统、日志聚合、分布式追踪、SLA监控、性能仪表板。适用于运维监控、系统可观测性等场景。"
update_agent "Q8-质量审核协调官" "质量审核协调官,Obsidian知识库质量保障专家。主动用于交叉检查增强工作、验证一致性、确保整个知识库的质量。适用于质量保障、内容审核等场景。"

echo "✨ Q series agents updated!"
