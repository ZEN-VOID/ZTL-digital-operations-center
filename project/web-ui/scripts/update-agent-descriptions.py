#!/usr/bin/env python3
"""
Script to update agent descriptions to be concise Chinese summaries (~150-200 chars).
Reads agent markdown files, extracts key capabilities, and generates standardized descriptions.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional


def extract_core_info(content: str, agent_name: str) -> Dict[str, str]:
    """Extract core information from agent markdown file."""

    # Try to find the "You are..." section
    you_are_match = re.search(r'You are (.+?),\s*(.+?)(?:\n\n|$)', content, re.DOTALL)

    # Try to find core positioning section
    positioning_match = re.search(r'## 🎯 Core Positioning\s*\n+(.+?)(?:\n#|$)', content, re.DOTALL | re.IGNORECASE)

    # Try to find mission/role section
    mission_match = re.search(r'\*\*(?:Your Mission|核心职责|主要职责|Core Responsibilities?)\*\*[:\s]*(.+?)(?:\n\n|$)', content, re.DOTALL)

    # Extract expertise/capabilities
    expertise_match = re.search(r'## 专业领域|## Professional Domain|## Core Expertise', content)

    core_info = {
        'role': you_are_match.group(2).strip() if you_are_match else '',
        'positioning': positioning_match.group(1).strip()[:200] if positioning_match else '',
        'mission': mission_match.group(1).strip()[:200] if mission_match else '',
        'agent_name': agent_name,
    }

    return core_info


def generate_chinese_description(core_info: Dict[str, str], agent_name: str, agent_id: str) -> str:
    """Generate concise Chinese description based on core info and agent role."""

    # Define templates for different agent types

    # Strategy Group (G series)
    if agent_id.startswith('G'):
        if agent_id == 'GG':
            return f"{agent_name},负责战略组整体规划与协调,统筹G0-G9专业智能体,提供战略级决策支持和多智能体编排能力。适用于复杂战略项目、业务转型规划、跨部门协作等场景。"
        elif agent_id == 'G0':
            return f"{agent_name},负责战略需求的深度分析与澄清,通过系统性访谈和需求建模,将模糊的业务目标转化为清晰的执行方案。适用于项目启动、战略规划、需求定义等场景。"
        elif agent_id == 'G1':
            return f"{agent_name},专注于经营数据分析与业务优化,通过数据驱动的方法识别经营问题、提供改进建议。适用于门店经营分析、成本优化、效率提升等场景。"
        elif agent_id == 'G2':
            return f"{agent_name},负责产品定位与优化策略,基于市场分析和用户洞察,提供产品创新和差异化竞争方案。适用于新品开发、产品重塑、市场定位等场景。"
        elif agent_id == 'G3':
            return f"{agent_name},专注于选址策略与区域扩张规划,通过商圈分析、人流预测、竞争评估,提供科学的选址决策支持。适用于新店选址、区域拓展、门店布局等场景。"
        elif agent_id == 'G4':
            return f"{agent_name},负责商业模式创新与盈利模式设计,通过价值链分析和商业逻辑重构,提供可持续的商业模式方案。适用于商业模式创新、盈利能力提升等场景。"
        elif agent_id == 'G5':
            return f"{agent_name},专注于连锁复制与标准化体系建设,将成功经验模式化,支持快速规模化扩张。适用于连锁扩张、标准化管理、复制体系建设等场景。"
        elif agent_id == 'G6':
            return f"{agent_name},负责数字化转型战略规划与IT架构设计,推动企业数字化升级和智能化改造。适用于数字化转型、系统规划、技术架构设计等场景。"
        elif agent_id == 'G7':
            return f"{agent_name},专注于流程优化与精细化管理,通过精益管理方法提升运营效率和管理水平。适用于流程优化、成本控制、效率提升等场景。"
        elif agent_id == 'G8':
            return f"{agent_name},负责人才发展与组织能力建设,设计培训体系和人才梯队,支撑业务快速发展。适用于人才培养、组织发展、培训体系建设等场景。"
        elif agent_id == 'G9':
            return f"{agent_name},专注于风险管理与合规审查,识别经营风险并提供预防和应对策略。适用于风险评估、合规管理、危机应对等场景。"

    # Creative Group (X series)
    elif agent_id.startswith('X'):
        if agent_id == 'X0':
            return f"{agent_name},负责创意项目需求分析与策划,将模糊创意转化为结构化需求文档。是创意生产流程的Phase 0,为下游执行团队提供清晰的项目规格。适用于视频制作、营销活动、品牌内容等创意项目启动阶段。"
        elif agent_id == 'X1':
            return f"{agent_name},专注于广告策略规划与创意提案,基于市场洞察和消费者心理,提供创新的广告解决方案。适用于广告campaign策划、品牌传播、营销活动设计等场景。"
        elif agent_id == 'X2':
            return f"{agent_name},负责营销文案创作与内容策划,撰写具有说服力和感染力的商业文案。适用于产品文案、营销推文、品牌故事、活动策划等场景。"
        elif agent_id == 'X3':
            return f"{agent_name},专注于设计模板解构与视觉元素分析,将优秀设计拆解为可复用的设计语言和模板。适用于设计系统建设、品牌VI规范、模板库构建等场景。"
        elif agent_id == 'X4':
            return f"{agent_name},负责品牌风格定义与视觉识别设计,建立统一的品牌视觉语言和设计规范。适用于品牌设计、VI系统、风格指南制定等场景。"
        elif agent_id == 'X5':
            return f"{agent_name},专注于社交媒体内容策划与运营,制定social内容矩阵和传播策略。适用于抖音、小红书、微信等平台的内容运营和增长策略。"
        elif agent_id == 'X6':
            return f"{agent_name},负责内容营销策略与传播规划,通过优质内容驱动用户增长和品牌认知。适用于内容矩阵搭建、传播策略、用户增长等场景。"
        elif agent_id.startswith('X1') and len(agent_id) == 3:  # X10-X15 AIGC series
            aigc_map = {
                'X10': '图片生成与处理',
                'X11': '视频生成',
                'X12': '音乐创作',
                'X13': '语音合成',
                'X14': '社交媒体视频剪辑',
                'X15': '视频编辑',
            }
            capability = aigc_map.get(agent_id, 'AIGC内容生成')
            return f"{agent_name},提供AIGC{capability}能力,通过AI技术快速生成高质量创意内容。适用于批量内容生产、快速原型制作、创意素材生成等场景。"

    # Intelligence Group (E series)
    elif agent_id.startswith('E'):
        if agent_id == 'EE':
            return f"{agent_name},负责情报组整体协调与数据分析战略规划,统筹E0-E8专业智能体,提供数据驱动的决策支持。适用于复杂调研项目、数据分析任务、跨团队协作等场景。"
        elif agent_id == 'E0':
            return f"{agent_name},负责调研需求分析与项目规划,设计调研方案和数据采集策略。是情报获取流程的Phase 0,为数据收集和分析奠定基础。"
        elif agent_id == 'E1':
            return f"{agent_name},专注于行业深度调研与竞品分析,通过多维度研究提供战略洞察。适用于市场调研、竞品分析、行业研究等场景。"
        elif agent_id == 'E2':
            return f"{agent_name},负责网页数据采集与信息爬取,使用Chrome DevTools自动化抓取网络数据。适用于竞品信息收集、价格监控、内容采集等场景。"
        elif agent_id == 'E3':
            return f"{agent_name},专注于美团平台数据分析,监控店铺运营数据和行业趋势。适用于美团运营优化、竞店分析、市场洞察等场景。"
        elif agent_id == 'E4':
            return f"{agent_name},负责数据分析与可视化报告制作,将原始数据转化为可视化洞察。适用于经营分析、数据报告、BI看板制作等场景。"
        elif agent_id == 'E5':
            return f"{agent_name},专注于API接口调用与数据集成,连接各类第三方服务和数据源。适用于系统集成、数据对接、API开发等场景。"
        elif agent_id == 'E8':
            return f"{agent_name},负责AI对话机器人开发与训练,构建智能客服和对话系统。适用于客服机器人、智能问答、对话流程设计等场景。"

    # Construction Group (Z series)
    elif agent_id.startswith('Z'):
        if agent_id == 'ZZ':
            return f"{agent_name},负责筹建组整体项目管理与进度协调,统筹Z0-Z5专业团队,确保门店筹建按时保质完成。适用于新店筹建、装修改造、项目管理等场景。"
        elif agent_id == 'Z0':
            return f"{agent_name},负责筹建需求分析与项目规划,制定详细的门店筹建方案和时间表。是筹建流程的Phase 0,为后续施工和装修奠定基础。"
        elif agent_id == 'Z1':
            return f"{agent_name},专注于平面布局设计与空间规划,优化动线和功能分区。适用于门店平面图设计、空间布局优化等场景。"
        elif agent_id == 'Z2':
            return f"{agent_name},负责BIM建模与三维可视化,创建数字化门店模型。适用于建筑信息模型构建、3D效果图制作等场景。"
        elif agent_id == 'Z3':
            return f"{agent_name},专注于室内设计与装修方案,打造符合品牌调性的就餐环境。适用于室内装修设计、软装搭配、风格定位等场景。"
        elif agent_id == 'Z4':
            return f"{agent_name},负责建筑动画与AIGC辅助设计,使用AI技术生成设计方案和效果图。适用于设计可视化、方案比选、客户提案等场景。"
        elif agent_id == 'Z5':
            return f"{agent_name},专注于施工图绘制与技术交底,提供精确的施工图纸和技术规范。适用于施工图设计、工程量统计、技术交底等场景。"

    # Development Group (F series)
    elif agent_id.startswith('F'):
        if agent_id == 'FF':
            return f"{agent_name},负责开发组整体技术架构与项目管理,统筹F0-F9开发团队,确保项目高质量交付。适用于技术规划、团队协作、项目管理等场景。"
        elif agent_id == 'F0':
            return f"{agent_name},负责需求分析与技术方案设计,将业务需求转化为可执行的技术规格。是开发流程的Phase 0,为后续编码和测试奠定基础。"
        else:
            return f"{agent_name},负责软件开发与技术实现,提供专业的编程和系统集成服务。适用于系统开发、功能实现、技术攻关等场景。"

    # Meituan Operations Group (V series)
    elif agent_id.startswith('V'):
        if agent_id == 'VV':
            return f"{agent_name},负责美团运营整体策略与团队协调,统筹V0-V5运营团队,提升平台经营效果。适用于美团战略规划、运营优化、团队管理等场景。"
        elif agent_id == 'V0':
            return f"{agent_name},负责美团运营需求分析与策略规划,制定针对性的运营方案。是运营流程的Phase 0,为后续执行提供清晰的策略方向。"
        else:
            return f"{agent_name},负责美团平台运营与效果优化,提升店铺曝光和订单转化。适用于美团店铺运营、活动策划、数据优化等场景。"

    # Supply Chain Group (C series)
    elif agent_id.startswith('C'):
        if agent_id == 'CC':
            return f"{agent_name},负责供应链战略规划与协调指挥,统筹C0-C5专业团队,推动供应链数字化转型。适用于供应链战略、跨部门协作、系统优化等场景。"
        elif agent_id == 'C0':
            return f"{agent_name},负责供应链需求分析与方案设计,识别供应链痛点并提供解决方案。是供应链优化的Phase 0,为后续执行奠定基础。"
        else:
            return f"{agent_name},负责供应链管理与运营优化,提升采购、库存、物流等环节效率。适用于供应链管理、成本控制、效率提升等场景。"

    # Admin Group (R series)
    elif agent_id.startswith('R'):
        if agent_id == 'RR':
            return f"{agent_name},负责行政组整体协调与运营管理,统筹R0-R8行政团队,支持企业平稳运行。适用于行政管理、综合事务、跨部门协作等场景。"
        elif agent_id == 'R0':
            return f"{agent_name},负责行政需求分析与方案制定,提供系统化的行政管理解决方案。是行政流程优化的Phase 0,为规范化管理奠定基础。"
        else:
            return f"{agent_name},负责行政事务处理与后勤支持,确保企业日常运营顺畅。适用于行政管理、后勤保障、资源协调等场景。"

    # QQ Command Center
    elif agent_id == 'QQ':
        return f"{agent_name},负责全局战略规划与多智能体协同编排,统筹所有业务组,提供端到端的项目解决方案。是系统最高指挥中枢,适用于复杂项目、战略决策、跨组协作等场景。"

    # Fallback
    return f"{agent_name},负责{core_info.get('role', '专业领域支持')},提供专业的解决方案和服务。适用于相关业务场景。"


def update_agent_description(file_path: Path, new_description: str) -> bool:
    """Update agent markdown file with new description."""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Find YAML frontmatter
        yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not yaml_match:
            print(f"⚠️  No YAML frontmatter found in {file_path.name}")
            return False

        yaml_content, body = yaml_match.groups()

        # Replace description in YAML
        # Handle multi-line descriptions
        yaml_content = re.sub(
            r'description:\s*["\']?(.*?)["\']?(?=\n\w+:|$)',
            f'description: {new_description}',
            yaml_content,
            flags=re.DOTALL
        )

        # Reconstruct file
        new_content = f"---\n{yaml_content}\n---\n{body}"
        file_path.write_text(new_content, encoding='utf-8')

        return True

    except Exception as e:
        print(f"❌ Error updating {file_path.name}: {e}")
        return False


def main():
    """Main function to update all agent descriptions."""

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    plugins_dir = project_root / 'plugins'
    claude_agents_dir = project_root / '.claude' / 'agents'

    # Agents that need updates (from previous analysis)
    agents_to_update = [
        'X0', 'G6', 'GG', 'X10', 'G0', 'X11', 'X12', 'X14', 'G7', 'X13',
        'G5', 'X3', 'X2', 'X6', 'X1', 'X4', 'G4', 'V5', 'Z4', 'X15',
        'G1', 'G2', 'G3', 'F1', 'E1', 'X5', 'Z0', 'V0', 'C0', 'R0', 'E0', 'F0', 'X8', 'QQ'
    ]

    updated_count = 0
    failed_count = 0

    print(f"🔄 Starting agent description updates...")
    print(f"📝 Total agents to update: {len(agents_to_update)}\n")

    # Search for agent files
    for agent_id in agents_to_update:
        agent_file = None
        agent_name = None

        # Search in plugins directory
        for group_dir in plugins_dir.iterdir():
            if not group_dir.is_dir():
                continue
            agents_dir = group_dir / 'agents'
            if not agents_dir.exists():
                continue

            for md_file in agents_dir.glob('*.md'):
                if md_file.name.startswith(agent_id + '-'):
                    agent_file = md_file
                    agent_name = md_file.stem.split('-', 1)[1]
                    break

            if agent_file:
                break

        # Search in .claude/agents
        if not agent_file and claude_agents_dir.exists():
            for md_file in claude_agents_dir.glob('*.md'):
                if md_file.name.startswith(agent_id + '-'):
                    agent_file = md_file
                    agent_name = md_file.stem.split('-', 1)[1]
                    break

        if not agent_file:
            print(f"❌ Agent file not found for {agent_id}")
            failed_count += 1
            continue

        # Read agent file
        content = agent_file.read_text(encoding='utf-8')
        core_info = extract_core_info(content, agent_name)

        # Generate new description
        new_desc = generate_chinese_description(core_info, agent_name, agent_id)

        # Update file
        if update_agent_description(agent_file, new_desc):
            print(f"✅ Updated {agent_id}-{agent_name}")
            print(f"   📄 {new_desc[:100]}...")
            updated_count += 1
        else:
            failed_count += 1

    print(f"\n✨ Update completed!")
    print(f"   ✅ Successfully updated: {updated_count}")
    print(f"   ❌ Failed: {failed_count}")

    if updated_count > 0:
        print(f"\n💡 Next step: Run 'npm run parse:agents' to regenerate agents-index.json")


if __name__ == '__main__':
    main()
