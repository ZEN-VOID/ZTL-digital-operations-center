#!/bin/bash
# Batch update agent descriptions from English to Chinese
# This version uses awk for more reliable multi-line handling

# Base directory
BASE_DIR="/Users/vincentlee/Desktop/ZTL数智化作战中心"

# Function to update a single agent file
update_agent_file() {
  local agent_id="$1"
  local new_description="$2"

  # Find the agent file
  local file=$(find "$BASE_DIR/plugins" -name "${agent_id}-*.md" 2>/dev/null | head -1)

  if [ -z "$file" ]; then
    echo "❌ ${agent_id}: File not found"
    return 1
  fi

  # Create temporary file
  local temp_file=$(mktemp)

  # Use awk to replace description
  awk -v new_desc="$new_description" '
    BEGIN {
      in_frontmatter = 0
      after_description = 0
      skip_lines = 0
    }
    /^---$/ {
      if (NR == 1) {
        in_frontmatter = 1
      } else if (in_frontmatter) {
        in_frontmatter = 0
      }
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
    skip_lines {
      next
    }
    { print }
  ' "$file" > "$temp_file"

  # Replace original file with updated content
  if [ -s "$temp_file" ]; then
    mv "$temp_file" "$file"
    echo "✅ ${agent_id}: Updated"
    return 0
  else
    rm "$temp_file"
    echo "❌ ${agent_id}: Update failed (empty file)"
    return 1
  fi
}

# Agent descriptions
update_agent_file "E3" "深度爬虫,负责企业级网页爬取策略规划,处理复杂的多页面导航、动态内容加载、反爬虫机制。提供分布式爬虫架构设计和大规模数据采集方案。适用于行业数据库构建、市场数据监控等场景。"
update_agent_file "E4" "深度情报分析,负责综合情报分析策略规划,整合多源数据进行深度洞察。提供竞品分析框架、市场趋势预测、战略决策支持。适用于战略研究、市场分析、风险评估等场景。"
update_agent_file "E5" "COS存储管理,负责腾讯云对象存储(COS)管理策略规划,提供文件上传、下载、图片处理、数据归档方案。支持AIGC内容存储、数据备份、CDN加速。适用于媒体资产管理、数据湖构建等场景。"
update_agent_file "E6" "Supabase数据库管理,负责Supabase PostgreSQL数据库管理策略规划,提供表结构设计、查询优化、数据迁移方案。支持实时数据订阅、行级安全策略。适用于应用数据管理、数据分析等场景。"
update_agent_file "EE" "情报组组长,负责情报组整体战略规划与协调,统筹E0-E6专业智能体,提供情报级决策支持和多智能体编排能力。适用于复杂情报项目、市场研究、数据采集等场景。"

update_agent_file "F2" "UI设计师,负责数字智能平台的UI/UX设计,专注于用户体验优化和界面设计规范。提供设计系统、原型设计、交互方案。适用于产品设计、界面优化、用户体验改进等场景。"
update_agent_file "F3" "全栈开发,负责数字智能协作平台的全栈开发,精通前后端技术栈。提供完整的应用开发解决方案,从需求分析到部署上线。适用于系统开发、功能实现、技术攻关等场景。"
update_agent_file "F4" "文档报告生成,负责技术文档和报告生成,专注于数字智能协作平台的文档体系建设。提供API文档、用户手册、技术规范。适用于文档编写、知识库建设等场景。"
update_agent_file "F5" "后端架构师,负责数字智能协作平台的后端架构设计,专注于系统可扩展性和性能优化。提供微服务架构、API设计、数据库优化方案。适用于系统架构设计、技术选型等场景。"
update_agent_file "F6" "数据库架构师,负责Supabase PostgreSQL数据库架构设计,专注于数据建模和性能优化。提供表结构设计、索引优化、查询性能调优方案。适用于数据架构设计、性能优化等场景。"
update_agent_file "F7" "API文档生成,负责数字智能协作平台的API文档生成,专注于接口规范和文档自动化。提供OpenAPI规范、接口文档、SDK生成方案。适用于API设计、接口文档管理等场景。"
update_agent_file "F8" "云架构师,负责腾讯云基础设施架构设计,专注于云原生架构和DevOps实践。提供云资源规划、容器编排、CI/CD流水线方案。适用于云迁移、基础设施优化等场景。"
update_agent_file "F9" "架构评审,负责数字智能协作平台的架构评审,专注于代码质量和架构合理性审查。提供架构建议、重构方案、技术债务管理。适用于代码审查、架构优化等场景。"
update_agent_file "F10" "Python专家,FastAPI后端开发专家,精通Pydantic V2、AsyncIO和Supabase集成。提供高性能异步API开发、数据验证、数据库交互方案。适用于后端开发、API设计、性能优化等场景。"
update_agent_file "F11" "TypeScript专家,Next.js 16 + React + TypeScript多智能体协作平台专家。精通Server Components、App Router、TypeScript高级特性。适用于前端开发、应用架构、类型安全等场景。"
update_agent_file "F12" "JavaScript专家,现代JavaScript (ES2024+)专家,深入掌握浏览器API和异步编程。提供原生JS解决方案、性能优化、浏览器兼容性方案。适用于前端开发、性能优化等场景。"
update_agent_file "F13" "代码审查专家,资深代码审查专家,专注于质量、安全性和可维护性。提供代码审查标准、安全漏洞检测、重构建议。适用于代码审查、质量保障、技术债务管理等场景。"
update_agent_file "F14" "测试工程师,测试自动化和质量保障专家。提供测试策略、自动化测试框架、持续集成方案。主动用于测试策略制定、测试用例生成、质量把关等场景。"
update_agent_file "F15" "性能优化专家,Web应用性能优化专家,擅长Core Web Vitals优化。提供性能分析、加载优化、渲染优化方案。适用于性能调优、用户体验提升等场景。"
update_agent_file "F16" "调试专家,系统级调试和问题诊断专家。提供深度调试技术、问题定位方法、根因分析方案。主动用于调试复杂问题、性能瓶颈分析等场景。"
update_agent_file "F17" "错误侦探,错误分析和根因诊断专家。提供错误模式识别、根因分析框架、预防措施建议。主动用于错误模式分析、问题预防等场景。"

update_agent_file "G8" "商业数据分析师,负责执行数据分析和生成商业报告,提供数据驱动的业务洞察。擅长数据可视化、趋势分析、业务建议。适用于数据分析、报告生成、决策支持等场景。"
update_agent_file "G9" "营销归因分析师,负责设计全面的营销归因框架,分析营销渠道效果和ROI。提供多触点归因模型、营销效果评估、预算优化方案。适用于营销分析、渠道优化、ROI提升等场景。"

update_agent_file "Q2" "技术文档专员,技术写作和内容创作专家。主动用于用户指南、教程、README文件、架构文档,提升内容清晰度和可访问性。适用于文档编写、技术传播等场景。"
update_agent_file "Q3" "变更日志专员,变更日志和发布说明专家。主动用于从git历史生成变更日志、创建发布说明、维护版本文档。适用于版本管理、发布流程等场景。"
update_agent_file "Q5" "上下文协调官,多智能体工作流和长时任务的上下文管理专家。主动用于复杂项目、会话协调、需要跨多个智能体保持上下文连续性的场景。"
update_agent_file "Q6" "项目流程协调官,项目工作流编排器。主动用于管理复杂的多步骤工作流,协调多个专业智能体按序工作,进行智能路由和负载验证。适用于复杂项目管理、流程自动化等场景。"
update_agent_file "Q7" "运维监控协调官,监控和可观测性基础设施专家。主动用于指标收集、告警系统、日志聚合、分布式追踪、SLA监控、性能仪表板。适用于运维监控、系统可观测性等场景。"
update_agent_file "Q8" "质量审核协调官,Obsidian知识库质量保障专家。主动用于交叉检查增强工作、验证一致性、确保整个知识库的质量。适用于质量保障、内容审核等场景。"

update_agent_file "R1" "财务管理员,负责专业的财务规划和预算管理,提供财务分析、成本控制、预算编制方案。适用于财务规划、成本优化、预算管理等场景。"
update_agent_file "R2" "人事管理员,负责专业的人力资源规划和劳动力管理,提供招聘计划、培训方案、绩效管理方案。适用于人力资源规划、团队建设等场景。"
update_agent_file "R3" "法务专家,负责专业的法律规划和风险管理,提供合同审查、法律咨询、合规建议。适用于法律事务、风险管理等场景。"
update_agent_file "R4" "秘书,负责专业的高管协助和协调支持,提供日程管理、会议组织、文件管理方案。适用于行政支持、协调管理等场景。"
update_agent_file "R5" "飞书管理员,负责专业的飞书平台协调规划,提供飞书应用配置、工作流自动化、团队协作方案。适用于飞书管理、协作优化等场景。"
update_agent_file "R6" "文件管理员,负责专业的文件和文档管理规划,提供文档分类、版本控制、归档方案。适用于文档管理、知识库建设等场景。"
update_agent_file "R7" "存储管理员,负责专业的存储基础设施规划和管理,提供存储架构设计、数据备份、容量规划方案。适用于存储管理、数据备份等场景。"
update_agent_file "RR" "行政组组长,负责财务、人力资源、法务、IT支持等行政任务管理,统筹R1-R7专业智能体,提供行政级决策支持。适用于行政管理、跨部门协调等场景。"

update_agent_file "V1" "运营管理员,负责创建美团管家平台的运营管理计划,设计运营配置方案、流程优化方案。适用于美团运营规划、配置管理等场景。"
update_agent_file "V2" "营销管理员,负责餐饮行业的营销策略规划和设计,提供营销活动方案、优惠券配置、RFM客户分群方案。适用于美团营销规划、活动设计等场景。"
update_agent_file "V4" "报表管理员,负责数据分析和报表规划设计,提供报表架构、数据查询、可视化方案。适用于美团数据分析、报表设计等场景。"

update_agent_file "X5" "Canvas图文排版师,专注于社交媒体内容策划与运营,制定social内容矩阵和传播策略。适用于抖音、小红书、微信等平台的内容运营和增长策略。"
update_agent_file "X7" "React前端设计师,负责专业的前端设计和UX/UI架构,精通React生态系统和现代前端开发。提供组件设计、交互方案、前端架构。适用于前端开发、用户体验优化等场景。"
update_agent_file "X8" "Gif动图设计师,专注于短视频视觉叙事的动画GIF艺术家。擅长创建引人入胜的循环动画、表情包、社交媒体内容。适用于社交媒体营销、品牌传播等场景。"
update_agent_file "XX" "创意组组长,负责创意工作协调、任务分解和质量保障,统筹X0-X16专业智能体。适用于创意项目管理、团队协调、跨职能协作等场景。"

update_agent_file "Z1" "平面图计划师,负责创建餐厅平面图配置和空间布局规划。提供功能分区、动线设计、尺寸标注方案。适用于餐厅筹建、空间规划等场景。"
update_agent_file "Z2" "空间设计师,负责使用Midjourney生成餐厅空间设计效果图。提供室内设计方案、风格定位、视觉呈现。适用于空间设计、效果图制作等场景。"
update_agent_file "Z3" "3D生成AIGC助手,负责将2D室内设计效果图转换为3D模型。提供3D建模、虚拟漫游、空间可视化方案。适用于3D建模、空间展示等场景。"

echo "✨ All agents updated!"
