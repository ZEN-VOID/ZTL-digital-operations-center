#!/usr/bin/env python3
"""
ResultAggregator - 结果汇总器
监控并汇总所有Worker的执行结果,生成完整报告

Version: 1.0.0
Created: 2025-11-01
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TaskResult:
    """任务结果数据结构"""
    task_id: str
    status: str
    execution_time: str
    duration_seconds: Optional[int]
    output_data: Dict[str, Any]
    summary: str
    errors: List[str]
    warnings: List[str]
    next_steps: List[str]


class ResultAggregator:
    """结果汇总器"""

    def __init__(self, project_name: str = "default-project"):
        """
        初始化结果汇总器

        Args:
            project_name: 项目名称
        """
        self.project_name = project_name
        self.task_queue_dir = Path(f"output/{project_name}/task-queue")
        self.results_dir = Path(f"output/{project_name}/results")
        self.report_path = Path(f"output/{project_name}/final-report.md")

        # 确保目录存在
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def monitor_and_aggregate(
        self,
        check_interval: int = 10,
        max_wait_time: int = 3600
    ) -> str:
        """
        持续监控任务队列,收集完成的结果并生成报告

        Args:
            check_interval: 检查间隔(秒)
            max_wait_time: 最大等待时间(秒)

        Returns:
            最终报告路径
        """
        print(f"🔍 开始监控任务执行...")
        print(f"   任务队列: {self.task_queue_dir}")
        print(f"   结果目录: {self.results_dir}")
        print(f"   检查间隔: {check_interval}秒")

        start_time = time.time()
        all_tasks = self._load_all_tasks()
        completed_results = {}

        if not all_tasks:
            print("⚠️  警告: 任务队列为空")
            return str(self.report_path)

        print(f"📋 总任务数: {len(all_tasks)}")
        self._print_task_status(all_tasks)

        # 持续监控直到所有任务完成或超时
        while not self._all_tasks_completed(all_tasks):
            elapsed_time = time.time() - start_time

            if elapsed_time > max_wait_time:
                print(f"⏰ 超时: 已等待 {elapsed_time:.0f} 秒,停止监控")
                break

            time.sleep(check_interval)

            # 重新加载任务状态
            all_tasks = self._load_all_tasks()

            # 收集新完成的结果
            for task in all_tasks:
                if task['status'] == 'completed' and task['task_id'] not in completed_results:
                    result = self._load_result(task['output_path'])
                    if result:
                        completed_results[task['task_id']] = result
                        print(f"✅ 收集到任务结果: {task['task_id']} - {task['description']}")

            # 打印进度
            completed_count = len([t for t in all_tasks if t['status'] == 'completed'])
            failed_count = len([t for t in all_tasks if t['status'] == 'failed'])
            print(f"📊 进度: {completed_count}/{len(all_tasks)} 完成, {failed_count} 失败")

        # 生成最终报告
        print("\n📝 生成最终报告...")
        final_report = self._generate_report(all_tasks, completed_results)

        # 保存报告
        with open(self.report_path, 'w', encoding='utf-8') as f:
            f.write(final_report)

        print(f"✅ 最终报告已保存: {self.report_path}")
        return str(self.report_path)

    def _load_all_tasks(self) -> List[Dict]:
        """加载所有任务配置"""
        tasks = []

        if not self.task_queue_dir.exists():
            return tasks

        for task_file in sorted(self.task_queue_dir.glob("task-*.json")):
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    task_data = json.load(f)
                    tasks.append(task_data)
            except Exception as e:
                print(f"❌ 读取任务文件失败: {task_file} - {e}")

        return tasks

    def _load_result(self, output_path: str) -> Optional[Dict]:
        """加载单个任务结果"""
        result_file = Path(output_path)

        if not result_file.exists():
            return None

        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 读取结果文件失败: {result_file} - {e}")
            return None

    def _all_tasks_completed(self, tasks: List[Dict]) -> bool:
        """检查是否所有任务都已完成"""
        if not tasks:
            return True

        return all(
            task['status'] in ['completed', 'failed']
            for task in tasks
        )

    def _print_task_status(self, tasks: List[Dict]):
        """打印任务状态摘要"""
        status_counts = {
            'pending': 0,
            'running': 0,
            'completed': 0,
            'failed': 0
        }

        for task in tasks:
            status = task.get('status', 'pending')
            status_counts[status] = status_counts.get(status, 0) + 1

        print("\n任务状态:")
        print(f"  ⏳ 待执行: {status_counts['pending']}")
        print(f"  🔄 执行中: {status_counts['running']}")
        print(f"  ✅ 已完成: {status_counts['completed']}")
        print(f"  ❌ 已失败: {status_counts['failed']}")
        print()

    def _generate_report(
        self,
        tasks: List[Dict],
        results: Dict[str, Dict]
    ) -> str:
        """
        生成最终报告

        Args:
            tasks: 所有任务列表
            results: 已收集的结果字典

        Returns:
            Markdown格式报告
        """
        report_lines = []

        # 报告标题
        report_lines.append(f"# 任务执行总报告")
        report_lines.append(f"\n**项目名称**: {self.project_name}")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**总任务数**: {len(tasks)}")

        # 执行摘要
        completed_tasks = [t for t in tasks if t['status'] == 'completed']
        failed_tasks = [t for t in tasks if t['status'] == 'failed']
        pending_tasks = [t for t in tasks if t['status'] in ['pending', 'running']]

        report_lines.append("\n## 📊 执行摘要\n")
        report_lines.append(f"- ✅ 已完成: {len(completed_tasks)}/{len(tasks)}")
        report_lines.append(f"- ❌ 已失败: {len(failed_tasks)}/{len(tasks)}")
        report_lines.append(f"- ⏳ 未完成: {len(pending_tasks)}/{len(tasks)}")

        # 计算总执行时间
        if completed_tasks:
            total_duration = sum(
                results.get(t['task_id'], {}).get('duration_seconds', 0)
                for t in completed_tasks
            )
            report_lines.append(f"- ⏱️  总执行时间: {total_duration} 秒 ({total_duration/60:.1f} 分钟)")

        # 按依赖关系排序任务
        sorted_tasks = self._topological_sort(tasks)

        # 详细结果
        report_lines.append("\n## 📋 详细结果\n")

        for i, task in enumerate(sorted_tasks, 1):
            task_id = task['task_id']
            result = results.get(task_id, {})

            report_lines.append(f"### 阶段{i}: {task['description']} ({task_id})")
            report_lines.append(f"\n**状态**: {self._format_status(task['status'])}")

            if task['dependencies']:
                report_lines.append(f"**依赖任务**: {', '.join(task['dependencies'])}")

            if task.get('started_at'):
                report_lines.append(f"**开始时间**: {task['started_at']}")

            if task.get('completed_at'):
                report_lines.append(f"**完成时间**: {task['completed_at']}")

            if result:
                # 输出摘要
                if result.get('summary'):
                    report_lines.append(f"\n**执行摘要**: {result['summary']}")

                # 输出数据
                if result.get('output_data'):
                    report_lines.append(f"\n**输出数据**:")
                    for key, value in result['output_data'].items():
                        report_lines.append(f"- {key}: {value}")

                # 错误信息
                if result.get('errors'):
                    report_lines.append(f"\n**错误信息**:")
                    for error in result['errors']:
                        report_lines.append(f"- ❌ {error}")

                # 警告信息
                if result.get('warnings'):
                    report_lines.append(f"\n**警告信息**:")
                    for warning in result['warnings']:
                        report_lines.append(f"- ⚠️ {warning}")

            # 输出文件路径
            report_lines.append(f"\n**输出文件**: `{task['output_path']}`")
            report_lines.append("")

        # 失败任务汇总
        if failed_tasks:
            report_lines.append("\n## ❌ 失败任务汇总\n")
            for task in failed_tasks:
                task_id = task['task_id']
                result = results.get(task_id, {})
                report_lines.append(f"### {task_id}: {task['description']}")

                if result and result.get('errors'):
                    for error in result['errors']:
                        report_lines.append(f"- {error}")
                report_lines.append("")

        # 总结
        report_lines.append("\n## 🎯 总结\n")

        if len(completed_tasks) == len(tasks):
            report_lines.append("✅ **所有任务已成功完成!**")
        elif failed_tasks:
            report_lines.append(f"⚠️ **部分任务失败** ({len(failed_tasks)}/{len(tasks)})")
        elif pending_tasks:
            report_lines.append(f"⏳ **部分任务未完成** ({len(pending_tasks)}/{len(tasks)})")

        # 下一步建议
        report_lines.append("\n### 下一步建议\n")
        if failed_tasks:
            report_lines.append("1. 检查失败任务的错误日志")
            report_lines.append("2. 修复问题后重新执行失败任务")
        if pending_tasks:
            report_lines.append("1. 检查未完成任务的状态")
            report_lines.append("2. 确认Worker是否正常运行")
        if len(completed_tasks) == len(tasks):
            report_lines.append("1. 查看各阶段的输出文件")
            report_lines.append("2. 整合最终交付物")

        return "\n".join(report_lines)

    def _topological_sort(self, tasks: List[Dict]) -> List[Dict]:
        """
        按依赖关系拓扑排序任务

        Args:
            tasks: 任务列表

        Returns:
            排序后的任务列表
        """
        # 构建依赖图
        task_dict = {task['task_id']: task for task in tasks}
        in_degree = {task['task_id']: 0 for task in tasks}

        # 计算入度
        for task in tasks:
            for dep in task.get('dependencies', []):
                if dep in in_degree:
                    in_degree[task['task_id']] += 1

        # 拓扑排序
        sorted_tasks = []
        queue = [tid for tid, degree in in_degree.items() if degree == 0]

        while queue:
            current_id = queue.pop(0)
            sorted_tasks.append(task_dict[current_id])

            # 更新依赖此任务的其他任务的入度
            for task in tasks:
                if current_id in task.get('dependencies', []):
                    in_degree[task['task_id']] -= 1
                    if in_degree[task['task_id']] == 0:
                        queue.append(task['task_id'])

        return sorted_tasks

    def _format_status(self, status: str) -> str:
        """格式化状态显示"""
        status_map = {
            'pending': '⏳ 待执行',
            'running': '🔄 执行中',
            'completed': '✅ 已完成',
            'failed': '❌ 已失败'
        }
        return status_map.get(status, status)

    def generate_summary_report(self) -> Dict[str, Any]:
        """生成JSON格式的摘要报告"""
        tasks = self._load_all_tasks()
        results = {}

        for task in tasks:
            result = self._load_result(task['output_path'])
            if result:
                results[task['task_id']] = result

        completed_tasks = [t for t in tasks if t['status'] == 'completed']
        failed_tasks = [t for t in tasks if t['status'] == 'failed']

        summary = {
            "project_name": self.project_name,
            "generated_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "completed_tasks": len(completed_tasks),
            "failed_tasks": len(failed_tasks),
            "success_rate": len(completed_tasks) / len(tasks) if tasks else 0,
            "tasks": [
                {
                    "task_id": task['task_id'],
                    "description": task['description'],
                    "status": task['status'],
                    "has_result": task['task_id'] in results
                }
                for task in tasks
            ]
        }

        return summary


def main():
    """命令行测试入口"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python result_aggregator.py <project_name> [--monitor]")
        sys.exit(1)

    project_name = sys.argv[1]
    monitor_mode = '--monitor' in sys.argv

    aggregator = ResultAggregator(project_name=project_name)

    if monitor_mode:
        # 监控模式: 持续监控并生成报告
        report_path = aggregator.monitor_and_aggregate(
            check_interval=10,
            max_wait_time=3600
        )
        print(f"\n✅ 最终报告: {report_path}")
    else:
        # 一次性生成报告
        tasks = aggregator._load_all_tasks()
        results = {}

        for task in tasks:
            result = aggregator._load_result(task['output_path'])
            if result:
                results[task['task_id']] = result

        report = aggregator._generate_report(tasks, results)

        with open(aggregator.report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ 报告已生成: {aggregator.report_path}")


if __name__ == "__main__":
    main()
