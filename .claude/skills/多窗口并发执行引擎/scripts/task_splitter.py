#!/usr/bin/env python3
"""
TaskSplitter - 智能任务分割器
将超长任务拆分为可并行执行的子任务,支持依赖关系管理

Version: 1.0.0
Created: 2025-11-01
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class SubTask:
    """子任务数据结构"""
    task_id: str
    description: str
    dependencies: List[str]
    status: str  # pending, running, completed, failed
    input_data: Dict[str, Any]
    execution_plan: str
    output_path: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    worker_window_index: Optional[int] = None
    estimated_duration: Optional[int] = None  # 预估执行时间(秒)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)


class TaskSplitter:
    """智能任务分割器"""

    def __init__(self, project_name: str = "default-project"):
        """
        初始化任务分割器

        Args:
            project_name: 项目名称,用于组织输出路径
        """
        self.project_name = project_name
        self.task_queue_dir = Path(f"output/{project_name}/task-queue")
        self.results_dir = Path(f"output/{project_name}/results")

        # 创建必需的目录
        self.task_queue_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def analyze_and_split(
        self,
        context: str,
        task_description: str,
        max_subtasks: int = 10
    ) -> List[SubTask]:
        """
        分析上下文和任务描述,智能分割为子任务

        Args:
            context: 当前完整上下文
            task_description: 任务描述
            max_subtasks: 最大子任务数量

        Returns:
            子任务列表
        """

        # 识别任务类型并应用相应的分割策略
        if self._is_data_analysis_task(task_description):
            return self._split_data_analysis_task(context, task_description)
        elif self._is_content_generation_task(task_description):
            return self._split_content_generation_task(context, task_description)
        elif self._is_research_task(task_description):
            return self._split_research_task(context, task_description)
        elif self._is_development_task(task_description):
            return self._split_development_task(context, task_description)
        else:
            return self._split_generic_task(context, task_description, max_subtasks)

    def _is_data_analysis_task(self, description: str) -> bool:
        """判断是否为数据分析任务"""
        keywords = ["数据分析", "数据处理", "数据清洗", "统计", "报表", "分析"]
        return any(keyword in description for keyword in keywords)

    def _is_content_generation_task(self, description: str) -> bool:
        """判断是否为内容生成任务"""
        keywords = ["生成", "创建", "设计", "写作", "文案", "海报", "视频"]
        return any(keyword in description for keyword in keywords)

    def _is_research_task(self, description: str) -> bool:
        """判断是否为调研任务"""
        keywords = ["调研", "研究", "分析", "调查", "收集", "爬虫", "采集"]
        return any(keyword in description for keyword in keywords)

    def _is_development_task(self, description: str) -> bool:
        """判断是否为开发任务"""
        keywords = ["开发", "实现", "编写", "重构", "优化", "修复", "代码"]
        return any(keyword in description for keyword in keywords)

    def _split_data_analysis_task(
        self,
        context: str,
        description: str
    ) -> List[SubTask]:
        """
        分割数据分析任务

        典型流程: 数据采集 → 数据清洗 → 数据分析 → 生成报告
        """
        subtasks = []
        timestamp = datetime.now().isoformat()

        # 阶段1: 数据采集
        subtasks.append(SubTask(
            task_id="T1",
            description="数据采集",
            dependencies=[],
            status="pending",
            input_data={
                "context_summary": self._extract_context_summary(context),
                "original_task": description
            },
            execution_plan="""
1. 根据任务描述确定数据源
2. 调用相应的API或爬虫工具采集数据
3. 将原始数据保存到CSV/JSON文件
4. 记录数据采集元数据(记录数、时间戳等)
            """.strip(),
            output_path=str(self.results_dir / "T1-result.json"),
            created_at=timestamp,
            estimated_duration=300  # 5分钟
        ))

        # 阶段2: 数据清洗
        subtasks.append(SubTask(
            task_id="T2",
            description="数据清洗",
            dependencies=["T1"],
            status="pending",
            input_data={
                "raw_data_path": "${T1.output_data.data_file}"
            },
            execution_plan="""
1. 读取T1采集的原始数据
2. 去除重复记录
3. 处理缺失值
4. 标准化数据格式
5. 保存清洗后的数据
            """.strip(),
            output_path=str(self.results_dir / "T2-result.json"),
            created_at=timestamp,
            estimated_duration=180  # 3分钟
        ))

        # 阶段3: 数据分析
        subtasks.append(SubTask(
            task_id="T3",
            description="数据分析",
            dependencies=["T2"],
            status="pending",
            input_data={
                "clean_data_path": "${T2.output_data.data_file}"
            },
            execution_plan="""
1. 读取T2清洗后的数据
2. 进行统计分析(均值、中位数、方差等)
3. 识别数据趋势和模式
4. 生成图表(如需要)
5. 保存分析结果
            """.strip(),
            output_path=str(self.results_dir / "T3-result.json"),
            created_at=timestamp,
            estimated_duration=240  # 4分钟
        ))

        # 阶段4: 生成报告
        subtasks.append(SubTask(
            task_id="T4",
            description="生成分析报告",
            dependencies=["T3"],
            status="pending",
            input_data={
                "analysis_result": "${T3.output_data.analysis_file}"
            },
            execution_plan="""
1. 读取T3的分析结果
2. 编写报告摘要
3. 整合图表和数据
4. 生成Markdown或PDF报告
5. 保存最终报告
            """.strip(),
            output_path=str(self.results_dir / "T4-result.json"),
            created_at=timestamp,
            estimated_duration=180  # 3分钟
        ))

        return subtasks

    def _split_content_generation_task(
        self,
        context: str,
        description: str
    ) -> List[SubTask]:
        """
        分割内容生成任务

        典型流程: 需求分析 → 内容策划 → 创作执行 → 审核优化
        """
        subtasks = []
        timestamp = datetime.now().isoformat()

        # 阶段1: 需求分析
        subtasks.append(SubTask(
            task_id="T1",
            description="内容需求分析",
            dependencies=[],
            status="pending",
            input_data={
                "context_summary": self._extract_context_summary(context),
                "original_task": description
            },
            execution_plan="""
1. 分析内容目标和受众
2. 确定内容类型和风格
3. 提取关键信息点
4. 定义内容结构
            """.strip(),
            output_path=str(self.results_dir / "T1-result.json"),
            created_at=timestamp,
            estimated_duration=120
        ))

        # 阶段2: 内容创作
        subtasks.append(SubTask(
            task_id="T2",
            description="内容创作执行",
            dependencies=["T1"],
            status="pending",
            input_data={
                "requirements": "${T1.output_data.requirements}"
            },
            execution_plan="""
1. 根据T1的需求分析创作内容
2. 应用指定的风格和格式
3. 生成初稿
4. 保存创作结果
            """.strip(),
            output_path=str(self.results_dir / "T2-result.json"),
            created_at=timestamp,
            estimated_duration=300
        ))

        # 阶段3: 审核优化
        subtasks.append(SubTask(
            task_id="T3",
            description="内容审核优化",
            dependencies=["T2"],
            status="pending",
            input_data={
                "draft_content": "${T2.output_data.content_file}"
            },
            execution_plan="""
1. 审核T2的创作内容
2. 检查质量和准确性
3. 优化表达和格式
4. 生成最终版本
            """.strip(),
            output_path=str(self.results_dir / "T3-result.json"),
            created_at=timestamp,
            estimated_duration=180
        ))

        return subtasks

    def _split_research_task(
        self,
        context: str,
        description: str
    ) -> List[SubTask]:
        """
        分割调研任务

        典型流程: 信息收集 → 数据整理 → 深度分析 → 报告撰写
        """
        subtasks = []
        timestamp = datetime.now().isoformat()

        # 阶段1: 信息收集
        subtasks.append(SubTask(
            task_id="T1",
            description="信息收集",
            dependencies=[],
            status="pending",
            input_data={
                "context_summary": self._extract_context_summary(context),
                "research_topic": description
            },
            execution_plan="""
1. 确定调研目标和范围
2. 收集相关资料和数据
3. 记录信息来源
4. 保存原始资料
            """.strip(),
            output_path=str(self.results_dir / "T1-result.json"),
            created_at=timestamp,
            estimated_duration=300
        ))

        # 阶段2: 数据整理
        subtasks.append(SubTask(
            task_id="T2",
            description="数据整理",
            dependencies=["T1"],
            status="pending",
            input_data={
                "raw_data": "${T1.output_data.collected_data}"
            },
            execution_plan="""
1. 整理T1收集的资料
2. 分类和标注数据
3. 提取关键信息
4. 建立数据索引
            """.strip(),
            output_path=str(self.results_dir / "T2-result.json"),
            created_at=timestamp,
            estimated_duration=240
        ))

        # 阶段3: 深度分析
        subtasks.append(SubTask(
            task_id="T3",
            description="深度分析",
            dependencies=["T2"],
            status="pending",
            input_data={
                "organized_data": "${T2.output_data.organized_file}"
            },
            execution_plan="""
1. 分析T2整理的数据
2. 识别趋势和模式
3. 得出关键发现
4. 提出建议和结论
            """.strip(),
            output_path=str(self.results_dir / "T3-result.json"),
            created_at=timestamp,
            estimated_duration=360
        ))

        # 阶段4: 报告撰写
        subtasks.append(SubTask(
            task_id="T4",
            description="调研报告撰写",
            dependencies=["T3"],
            status="pending",
            input_data={
                "analysis_result": "${T3.output_data.findings}"
            },
            execution_plan="""
1. 撰写调研报告
2. 整合分析结果
3. 添加图表和引用
4. 生成最终报告
            """.strip(),
            output_path=str(self.results_dir / "T4-result.json"),
            created_at=timestamp,
            estimated_duration=240
        ))

        return subtasks

    def _split_development_task(
        self,
        context: str,
        description: str
    ) -> List[SubTask]:
        """
        分割开发任务

        典型流程: 需求分析 → 设计方案 → 编码实现 → 测试验证
        """
        subtasks = []
        timestamp = datetime.now().isoformat()

        # 阶段1: 需求分析
        subtasks.append(SubTask(
            task_id="T1",
            description="需求分析",
            dependencies=[],
            status="pending",
            input_data={
                "context_summary": self._extract_context_summary(context),
                "feature_description": description
            },
            execution_plan="""
1. 分析功能需求
2. 识别技术约束
3. 列出依赖和前置条件
4. 定义验收标准
            """.strip(),
            output_path=str(self.results_dir / "T1-result.json"),
            created_at=timestamp,
            estimated_duration=180
        ))

        # 阶段2: 设计方案
        subtasks.append(SubTask(
            task_id="T2",
            description="技术设计",
            dependencies=["T1"],
            status="pending",
            input_data={
                "requirements": "${T1.output_data.requirements}"
            },
            execution_plan="""
1. 设计技术架构
2. 定义接口和数据结构
3. 选择技术栈
4. 编写设计文档
            """.strip(),
            output_path=str(self.results_dir / "T2-result.json"),
            created_at=timestamp,
            estimated_duration=240
        ))

        # 阶段3: 编码实现
        subtasks.append(SubTask(
            task_id="T3",
            description="编码实现",
            dependencies=["T2"],
            status="pending",
            input_data={
                "design_doc": "${T2.output_data.design_file}"
            },
            execution_plan="""
1. 根据T2设计编写代码
2. 实现核心功能
3. 编写单元测试
4. 代码审查和优化
            """.strip(),
            output_path=str(self.results_dir / "T3-result.json"),
            created_at=timestamp,
            estimated_duration=600
        ))

        # 阶段4: 测试验证
        subtasks.append(SubTask(
            task_id="T4",
            description="测试验证",
            dependencies=["T3"],
            status="pending",
            input_data={
                "code_files": "${T3.output_data.code_paths}"
            },
            execution_plan="""
1. 运行单元测试
2. 执行集成测试
3. 验证功能完整性
4. 生成测试报告
            """.strip(),
            output_path=str(self.results_dir / "T4-result.json"),
            created_at=timestamp,
            estimated_duration=300
        ))

        return subtasks

    def _split_generic_task(
        self,
        context: str,
        description: str,
        max_subtasks: int
    ) -> List[SubTask]:
        """
        通用任务分割策略

        将任务分为N个相等的子任务
        """
        subtasks = []
        timestamp = datetime.now().isoformat()

        # 简单分割: 将任务平均分为N个子任务
        for i in range(1, max_subtasks + 1):
            task_id = f"T{i}"
            prev_task = f"T{i-1}" if i > 1 else None

            subtasks.append(SubTask(
                task_id=task_id,
                description=f"子任务{i}: {description} (阶段{i}/{max_subtasks})",
                dependencies=[prev_task] if prev_task else [],
                status="pending",
                input_data={
                    "context_summary": self._extract_context_summary(context),
                    "stage": f"{i}/{max_subtasks}"
                },
                execution_plan=f"执行任务的第{i}阶段",
                output_path=str(self.results_dir / f"{task_id}-result.json"),
                created_at=timestamp,
                estimated_duration=300
            ))

        return subtasks

    def _extract_context_summary(self, context: str, max_length: int = 1000) -> str:
        """提取上下文摘要"""
        if len(context) <= max_length:
            return context

        # 截取前max_length字符
        summary = context[:max_length]
        return f"{summary}\n\n... (上下文已截断,完整内容共 {len(context)} 字符)"

    def save_subtasks(self, subtasks: List[SubTask]) -> List[Path]:
        """
        保存子任务到task-queue目录

        Args:
            subtasks: 子任务列表

        Returns:
            保存的文件路径列表
        """
        saved_paths = []

        for task in subtasks:
            task_file = self.task_queue_dir / f"task-{task.task_id}.json"

            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(task.to_dict(), f, indent=2, ensure_ascii=False)

            saved_paths.append(task_file)
            print(f"✅ 已保存任务: {task_file}")

        return saved_paths

    def load_all_tasks(self) -> List[SubTask]:
        """加载所有任务"""
        tasks = []

        for task_file in sorted(self.task_queue_dir.glob("task-*.json")):
            with open(task_file, 'r', encoding='utf-8') as f:
                task_data = json.load(f)
                tasks.append(SubTask(**task_data))

        return tasks

    def update_task_status(
        self,
        task_id: str,
        status: str,
        worker_window_index: Optional[int] = None
    ):
        """更新任务状态"""
        task_file = self.task_queue_dir / f"task-{task_id}.json"

        if not task_file.exists():
            raise FileNotFoundError(f"任务文件不存在: {task_file}")

        with open(task_file, 'r', encoding='utf-8') as f:
            task_data = json.load(f)

        task_data['status'] = status

        if status == 'running':
            task_data['started_at'] = datetime.now().isoformat()
            if worker_window_index:
                task_data['worker_window_index'] = worker_window_index
        elif status == 'completed':
            task_data['completed_at'] = datetime.now().isoformat()

        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)

        print(f"✅ 已更新任务状态: {task_id} → {status}")


def main():
    """命令行测试入口"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python task_splitter.py <project_name> <task_description>")
        sys.exit(1)

    project_name = sys.argv[1]
    task_description = " ".join(sys.argv[2:])

    splitter = TaskSplitter(project_name=project_name)

    # 模拟上下文
    context = f"""
当前任务: {task_description}
上下文信息: 这是一个测试任务,用于验证任务分割器的功能。
    """.strip()

    # 分割任务
    subtasks = splitter.analyze_and_split(context, task_description)

    # 保存任务
    saved_paths = splitter.save_subtasks(subtasks)

    # 输出摘要
    print(f"\n✅ 任务分割完成!")
    print(f"项目名称: {project_name}")
    print(f"子任务数量: {len(subtasks)}")
    print(f"任务队列目录: {splitter.task_queue_dir}")
    print(f"结果输出目录: {splitter.results_dir}")

    print("\n子任务列表:")
    for task in subtasks:
        deps = ", ".join(task.dependencies) if task.dependencies else "无"
        print(f"  - {task.task_id}: {task.description} (依赖: {deps})")


if __name__ == "__main__":
    main()
