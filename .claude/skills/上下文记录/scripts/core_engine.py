#!/usr/bin/env python3
"""
上下求索 - 核心执行引擎
基于MANUS上下文工程原则的智能上下文管理系统

版本: v3.0.0
更新: 2025-10-31
"""

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Any


@dataclass
class ManusResult:
    """MANUS执行结果"""
    type: str              # 识别的类型
    level: str             # 分类级别(全局/项目)
    target_file: str       # 目标文件路径
    timestamp: str         # ISO 8601时间戳
    detection_method: str  # 识别方式(智能识别/显式指定)
    detection_reason: str  # 识别依据

    # ERROR类型特殊字段
    error_id: Optional[str] = None
    error_stats: Optional[Dict[str, Any]] = None

    # 通用统计
    section_stats: Optional[Dict[str, Any]] = None


class ManusEngine:
    """MANUS核心执行引擎"""

    # 类型图标映射
    TYPE_ICONS = {
        "focus": "🎯",
        "todo": "📋",
        "process": "⚙️",
        "error": "❌",
        "success": "✅",
        "insights": "🧠",
        "patterns": "🔍",
        "context": "📊",
        "memory": "🧠",
        "snapshot": "📸"
    }

    # 错误类型
    ERROR_TYPES = [
        "LOGIC", "SYNTAX", "PERMISSION",
        "TOOL_USE", "FILE_OP", "INTEGRATION", "PERFORMANCE"
    ]

    # 严重级别
    SEVERITY_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    def __init__(self, project_root: Path = Path.cwd()):
        """初始化引擎"""
        self.project_root = project_root
        self.context_dir = project_root / "context"
        self.errors_file = self.context_dir / "errors" / "ERRORS.jsonl"

    def execute(
        self,
        content: str,
        explicit_type: Optional[str] = None
    ) -> ManusResult:
        """
        执行MANUS上下文管理操作

        Args:
            content: 用户输入内容
            explicit_type: 显式指定的类型(可选)

        Returns:
            ManusResult: 执行结果
        """
        # Step 1: 类型识别
        if explicit_type:
            manus_type = explicit_type.lower()
            detection_method = "显式指定"
            detection_reason = ""
        else:
            manus_type, detection_reason = self.auto_detect_type(content)
            detection_method = "智能识别"

        # Step 2: 分类判断
        level, target_file = self.classify_level(content)

        # Step 3: 生成时间戳
        timestamp = datetime.now().isoformat()

        # Step 4: 处理不同类型
        if manus_type == "error":
            result = self._handle_error_type(content, level, timestamp)
        else:
            result = self._handle_general_type(
                content, manus_type, level, target_file, timestamp
            )

        # Step 5: 返回结果
        return ManusResult(
            type=manus_type,
            level=level,
            target_file=target_file,
            timestamp=timestamp,
            detection_method=detection_method,
            detection_reason=detection_reason,
            **result
        )

    def auto_detect_type(self, content: str) -> Tuple[str, str]:
        """
        智能识别内容类型

        Args:
            content: 用户输入内容

        Returns:
            (type, reason): 类型和识别依据
        """
        content_lower = content.lower()
        reasons = []

        # 1. ERROR类型识别 (最高优先级)
        error_keywords = [
            "错误", "失败", "报错", "bug", "issue",
            "异常", "崩溃", "crash", "exception",
            "不工作", "无法", "无效"
        ]
        error_structures = ["预期", "实际", "堆栈", "stack", "恢复", "修复"]

        if any(kw in content_lower for kw in error_keywords):
            reasons.append(f"包含错误关键词")
        if any(kw in content_lower for kw in error_structures):
            reasons.append("包含错误结构特征")

        if reasons:
            return ("error", ", ".join(reasons))
        reasons.clear()

        # 2. SUCCESS类型识别
        success_keywords = [
            "成功", "解决了", "实现了", "完成",
            "突破", "优化", "改进", "效果", "收益", "提升"
        ]
        success_structures = ["→", "从", "到"]

        if any(kw in content_lower for kw in success_keywords):
            reasons.append("包含成功关键词")
        if any(kw in content for kw in success_structures):
            reasons.append("包含改进数据结构")

        if reasons:
            return ("success", ", ".join(reasons))
        reasons.clear()

        # 3. INSIGHTS类型识别
        insights_keywords = [
            "洞察", "发现", "理解", "原理",
            "机制", "为什么", "深度", "本质", "根本"
        ]

        if any(kw in content_lower for kw in insights_keywords):
            return ("insights", "包含洞察关键词")

        # 4. PATTERNS类型识别
        patterns_keywords = [
            "模式", "pattern", "重复",
            "最佳实践", "反模式", "anti-pattern", "设计模式"
        ]

        if any(kw in content_lower for kw in patterns_keywords):
            return ("patterns", "包含模式关键词")

        # 5. CONTEXT类型识别
        context_keywords = [
            "上下文", "context", "token",
            "监控", "优化", "压缩", "溢出", "容量", "使用率"
        ]

        if any(kw in content_lower for kw in context_keywords):
            return ("context", "包含上下文监控关键词")

        # 6. MEMORY类型识别
        memory_keywords = [
            "记忆", "memory", "记住",
            "长期", "持久化", "保存", "重要", "关键决策"
        ]

        if any(kw in content_lower for kw in memory_keywords):
            return ("memory", "包含记忆管理关键词")

        # 7. SNAPSHOT类型识别
        snapshot_keywords = [
            "快照", "snapshot", "备份",
            "版本", "恢复", "回退", "checkpoint", "保存点"
        ]

        if any(kw in content_lower for kw in snapshot_keywords):
            return ("snapshot", "包含快照管理关键词")

        # 8. TODO类型识别
        todo_keywords = [
            "待办", "任务", "需要", "要做",
            "todo", "清单", "checklist"
        ]
        todo_structures = content.count("-") >= 2 or content.count("•") >= 2

        if any(kw in content_lower for kw in todo_keywords):
            reasons.append("包含任务关键词")
        if todo_structures:
            reasons.append("列表结构")

        if reasons:
            return ("todo", ", ".join(reasons))
        reasons.clear()

        # 9. FOCUS类型识别
        focus_keywords = [
            "专注", "集中", "当前任务", "正在做",
            "注意力", "焦点", "优先级", "接下来", "计划做"
        ]
        focus_structures = (
            "小时" in content or "h" in content_lower or
            "成功标准" in content
        )

        if any(kw in content_lower for kw in focus_keywords):
            reasons.append("包含焦点关键词")
        if focus_structures:
            reasons.append("包含时间/成功标准")

        if reasons:
            return ("focus", ", ".join(reasons))
        reasons.clear()

        # 10. PROCESS类型识别
        process_keywords = [
            "流程", "步骤", "过程", "工作流",
            "workflow", "pipeline", "执行", "操作"
        ]
        process_structures = "→" in content or "step" in content_lower

        if any(kw in content_lower for kw in process_keywords):
            reasons.append("包含流程关键词")
        if process_structures:
            reasons.append("包含步骤结构")

        if reasons:
            return ("process", ", ".join(reasons))

        # 11. 默认策略
        if len(content) < 100:
            return ("focus", "基于内容长度判断(简短描述)")
        elif content.count("\n") >= 3:
            return ("todo", "基于内容结构判断(多行列表)")
        else:
            return ("insights", "基于内容综合判断(详细叙述)")

    def classify_level(self, content: str) -> Tuple[str, str]:
        """
        双层级分类判断

        Args:
            content: 用户输入内容

        Returns:
            (level, target_file): 级别和目标文件路径
        """
        content_lower = content.lower()

        # Step 1: 强匹配项目级别
        project_keywords = [
            "本项目", "当前项目", "当前业务",
            "项目配置", "本地开发"
        ]

        if any(kw in content_lower for kw in project_keywords):
            return ("项目级别", "CLAUDE.md")

        # Step 2: 检测项目文件路径
        project_paths = [
            ".claude/", "plugins/", "prps/",
            "context/", "output/", "reports/"
        ]

        if any(path in content_lower for path in project_paths):
            return ("项目级别", "CLAUDE.md")

        # Step 3: 强匹配全局级别
        global_keywords = [
            "跨项目", "通用", "框架",
            "最佳实践", "可复用",
            "技术洞察", "工具使用"
        ]

        if any(kw in content_lower for kw in global_keywords):
            return ("全局级别", "~/.claude/CLAUDE.md")

        # Step 4: 默认策略(项目级别更安全)
        return ("项目级别", "CLAUDE.md")

    def _handle_error_type(
        self,
        content: str,
        level: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """
        处理ERROR类型

        Returns:
            包含error_id和error_stats的字典
        """
        # 确保目录存在
        self.errors_file.parent.mkdir(parents=True, exist_ok=True)

        # 生成错误ID
        error_count = self._count_errors()
        date_str = datetime.now().strftime("%Y%m%d")
        error_id = f"ERR-{date_str}-{error_count + 1:03d}"

        # 解析MANUS五步法(简化版,实际应更详细)
        error_json = {
            "error_id": error_id,
            "timestamp": timestamp,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "manus": self._parse_manus_fields(content),
            "metadata": {
                "level": level,
                "project": str(self.project_root.name)
            }
        }

        # 写入ERRORS.jsonl
        with open(self.errors_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_json, ensure_ascii=False) + "\n")

        # 统计信息
        error_stats = {
            "total_errors": error_count + 1,
            "error_file": str(self.errors_file),
            "line_number": error_count + 1
        }

        return {
            "error_id": error_id,
            "error_stats": error_stats
        }

    def _handle_general_type(
        self,
        content: str,
        manus_type: str,
        level: str,
        target_file: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """
        处理一般类型(非ERROR)

        Returns:
            包含section_stats的字典
        """
        # 生成条目
        icon = self.TYPE_ICONS.get(manus_type, "📝")
        type_name = manus_type.upper()

        entry = f"""
#### 🕐 {timestamp} {icon} {type_name}: [待填充标题]

{content}

<!-- Cache Breakpoint: {type_name} section updated -->
"""

        # 注意: 实际实现应该调用Write/Edit工具来修改CLAUDE.md
        # 这里仅返回生成的条目内容

        section_stats = {
            "entry_preview": entry[:200],
            "entry_length": len(entry)
        }

        return {
            "section_stats": section_stats
        }

    def _count_errors(self) -> int:
        """统计已有错误数量"""
        if not self.errors_file.exists():
            return 0

        with open(self.errors_file, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    def _parse_manus_fields(self, content: str) -> Dict[str, Any]:
        """
        解析MANUS五步法字段(简化版)

        实际实现应该更详细地解析用户输入
        """
        return {
            "mistake": {
                "type": "LOGIC",  # 应从内容中提取
                "severity": "HIGH",
                "failed_action": "待解析",
                "context": content[:500]
            },
            "acknowledgment": {
                "root_cause": "待解析",
                "wrong_understanding": "待解析",
                "correct_understanding": "待解析"
            },
            "new_understanding": {
                "key_insights": ["待解析"]
            },
            "updated_approach": {
                "correct_workflow": ["待解析"]
            },
            "systematic_prevention": {
                "prevention_rules": ["待解析"]
            }
        }


def main():
    """命令行接口(用于测试)"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python core_engine.py <content> [type]")
        sys.exit(1)

    content = sys.argv[1]
    explicit_type = sys.argv[2] if len(sys.argv) > 2 else None

    engine = ManusEngine()
    result = engine.execute(content, explicit_type)

    print("\n=== MANUS执行结果 ===")
    print(f"🤖 类型识别: {engine.TYPE_ICONS[result.type]} {result.type.upper()} ({result.detection_method})")
    if result.detection_reason:
        print(f"💡 识别依据: {result.detection_reason}")
    print(f"📊 分类级别: {result.level}")
    print(f"📁 目标文件: {result.target_file}")
    print(f"🕐 时间戳: {result.timestamp}")

    if result.error_id:
        print(f"\n❌ 错误信息:")
        print(f"  错误ID: {result.error_id}")
        print(f"  总错误数: {result.error_stats['total_errors']}")
        print(f"  存储位置: {result.error_stats['error_file']}:#{result.error_stats['line_number']}")


if __name__ == "__main__":
    main()
