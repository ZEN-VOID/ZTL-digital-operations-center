#!/usr/bin/env python3
"""
Wan Execute Engine - E8执行引擎（通义万相）
基于JSON执行计划自动化批量生成E8图生视频（通义万相2.5）

核心功能：
- 加载和验证JSON执行计划
- 批量处理任务（支持配置化批次大小和并发）
- Checkpoint机制（支持断点续传）
- 指数退避重试策略（2s, 4s, 8s）
- 异步任务轮询和视频下载
- 音频配置处理（自动配音/自定义音频/无声）
- 视频特效应用
- 质量检查和元数据生成

使用方法:
  python wan-execute.py --plan output/tongyi-wanxiang/plans/wan-i2v-template.json
"""

import sys
import json
import argparse
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import yaml

# 动态导入wan-base模块
api_file_path = Path(__file__).parent / "wan-base.py"
import importlib.util
spec = importlib.util.spec_from_file_location("wan_base", api_file_path)
wan_module = importlib.util.module_from_spec(spec)
sys.modules["wan_base"] = wan_module
spec.loader.exec_module(wan_module)
WanAPIClient = wan_module.WanAPIClient


class E8ExecutionEngine:
    """E8执行引擎 - 批量图生视频（通义万相）"""

    def __init__(self, plan_path: str):
        """
        初始化执行引擎

        Args:
            plan_path: 执行计划JSON文件路径
        """
        self.plan_path = Path(plan_path)
        self.plan = None
        self.api = None  # 延迟初始化

        # 执行状态
        self.total_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.execution_log = []

        # Checkpoint
        self.checkpoint_data = {
            "completed_task_ids": [],
            "failed_task_ids": [],
            "last_update": None
        }

    def load_plan(self) -> bool:
        """加载执行计划"""
        try:
            print(f"📄 加载执行计划: {self.plan_path}")

            if not self.plan_path.exists():
                print(f"❌ 错误: 执行计划文件不存在 - {self.plan_path}")
                return False

            with open(self.plan_path, 'r', encoding='utf-8') as f:
                self.plan = json.load(f)

            # 验证必需字段
            required_fields = ["plan_id", "agent_id", "batches", "output_config", "api_config"]
            for field in required_fields:
                if field not in self.plan:
                    print(f"❌ 错误: 执行计划缺少必需字段 '{field}'")
                    return False

            # 验证agent_id
            agent_id = self.plan.get("agent_id")
            if agent_id not in ["E8", "E9"]:
                print(f"❌ 错误: 此执行引擎仅支持E8/E9智能体（通义万相API），当前计划为: {agent_id}")
                return False

            # 初始化API客户端
            api_config = self.plan.get("api_config", {})
            self.api = WanAPIClient(
                endpoint=api_config.get("endpoint", "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"),
                query_endpoint=api_config.get("query_endpoint", "https://dashscope.aliyuncs.com/api/v1/tasks"),
                model=api_config.get("model", "wan2.5-i2v-preview")
            )

            # 更新查询配置
            self.api.default_query_interval = api_config.get("query_interval_seconds", 5)
            self.api.default_max_wait_time = api_config.get("max_query_duration_seconds", 600)

            # 统计任务数
            self.total_tasks = sum(
                len(batch.get("tasks", []))
                for batch in self.plan.get("batches", [])
            )

            print(f"✅ 执行计划加载成功")
            print(f"   📋 计划ID: {self.plan.get('plan_id')}")
            print(f"   🎯 项目名称: {self.plan.get('project_name')}")
            print(f"   📦 批次数量: {len(self.plan.get('batches', []))}")
            print(f"   🎬 任务总数: {self.total_tasks}")

            return True

        except json.JSONDecodeError as e:
            print(f"❌ 错误: JSON格式错误 - {e}")
            return False
        except Exception as e:
            print(f"❌ 错误: 加载执行计划失败 - {e}")
            return False

    def validate_input_files(self) -> bool:
        """验证输入文件完整性"""
        print("\n🔍 验证输入文件...")

        # 检查输入图像路径和音频文件
        missing_files = []
        for batch in self.plan.get("batches", []):
            for task in batch.get("tasks", []):
                input_data = task.get("input_data", {})
                params = task.get("parameters", {})

                # 检查图片（如果使用本地路径）
                image_path = input_data.get("image_path")
                if image_path and not input_data.get("image_url"):
                    if not Path(image_path).exists():
                        missing_files.append(f"图片: {image_path}")

                # 检查音频文件（如果使用自定义音频）
                audio_config = params.get("audio_config", {})
                if audio_config.get("audio_mode") == "custom_audio":
                    audio_file_path = audio_config.get("audio_file_path")
                    if audio_file_path and not Path(audio_file_path).exists():
                        missing_files.append(f"音频: {audio_file_path}")

        if missing_files:
            print(f"⚠️  警告: 发现 {len(missing_files)} 个缺失的输入文件")
            for f in missing_files[:5]:  # 只显示前5个
                print(f"   - {f}")
            if len(missing_files) > 5:
                print(f"   ... 还有 {len(missing_files) - 5} 个")
            return False

        print("   ✅ 所有输入文件完整")
        return True

    def setup_output_directories(self):
        """创建输出目录结构"""
        print("\n📁 创建输出目录...")

        output_config = self.plan.get("output_config", {})
        base_path = Path(output_config.get("base_path", "output/temp"))
        subdirs = output_config.get("subdirs", {
            "raw": "raw",
            "final": "final",
            "review": "review",
            "rejected": "rejected",
            "comparisons": "comparisons",
            "logs": "logs",
            "audio": "audio"  # 通义万相特有：音频文件目录
        })

        # 创建所有子目录
        for subdir_key, subdir_name in subdirs.items():
            subdir_path = base_path / subdir_name
            subdir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {subdir_path}")

        # 保存输出路径
        self.output_base = base_path
        self.output_subdirs = {k: base_path / v for k, v in subdirs.items()}

    async def execute_single_task(self, task: Dict[str, Any], retry_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个任务（带重试）

        Args:
            task: 任务配置
            retry_config: 重试配置

        Returns:
            任务执行结果
        """
        task_id = task.get("task_id")
        task_name = task.get("task_name", task_id)

        retry_attempts = retry_config.get("retry_attempts", 3)
        retry_delays = retry_config.get("retry_delay_seconds", [2, 4, 8])

        print(f"   🎬 任务 {task_id}: {task_name}...")

        for attempt in range(retry_attempts):
            try:
                # 构建任务数据
                task_data = {
                    "input_data": task.get("input_data", {}),
                    "parameters": task.get("parameters", {})
                }

                # 确定输出路径
                output_config = task.get("output_config", {})
                output_filename = output_config.get("output_filename", f"{task_id}.mp4")

                # 根据配置决定保存位置
                save_to_raw = output_config.get("save_to_raw", True)
                save_to_final = output_config.get("save_to_final", False)

                output_dir = self.output_subdirs["raw"] if save_to_raw else self.output_subdirs["final"]
                output_path = output_dir / output_filename

                # 调用API生成视频
                result = self.api.generate_video(
                    task_data=task_data,
                    output_path=output_path,
                    retry_config=retry_config
                )

                if result["success"]:
                    # 如果需要同时保存到final
                    if save_to_raw and save_to_final:
                        final_path = self.output_subdirs["final"] / output_filename
                        import shutil
                        shutil.copy2(output_path, final_path)
                        print(f"      ✅ 已同步到final: {final_path}")

                    return {
                        "task_id": task_id,
                        "task_name": task_name,
                        "success": True,
                        "video_path": result.get("video_path"),
                        "video_url": result.get("video_url"),
                        "processing_time": result.get("processing_time", 0),
                        "attempts": attempt + 1
                    }
                else:
                    error_msg = result.get("error", "未知错误")
                    print(f"      ⚠️  尝试 {attempt + 1}/{retry_attempts} 失败: {error_msg}")

                    # 如果还有重试机会，等待后重试
                    if attempt < retry_attempts - 1:
                        delay = retry_delays[min(attempt, len(retry_delays) - 1)]
                        print(f"      ⏱️  等待 {delay}秒后重试...")
                        await asyncio.sleep(delay)
                    else:
                        # 最后一次尝试失败
                        return {
                            "task_id": task_id,
                            "task_name": task_name,
                            "success": False,
                            "error": error_msg,
                            "attempts": retry_attempts
                        }

            except Exception as e:
                print(f"      ❌ 尝试 {attempt + 1}/{retry_attempts} 异常: {str(e)}")

                if attempt < retry_attempts - 1:
                    delay = retry_delays[min(attempt, len(retry_delays) - 1)]
                    await asyncio.sleep(delay)
                else:
                    return {
                        "task_id": task_id,
                        "task_name": task_name,
                        "success": False,
                        "error": str(e),
                        "attempts": retry_attempts
                    }

    async def execute_batch(self, batch: Dict[str, Any], batch_index: int) -> List[Dict[str, Any]]:
        """
        执行批次任务（并发处理）

        Args:
            batch: 批次配置
            batch_index: 批次索引

        Returns:
            批次执行结果列表
        """
        batch_id = batch.get("batch_id")
        batch_name = batch.get("batch_name", f"批次{batch_id}")
        tasks = batch.get("tasks", [])

        print(f"\n📦 批次 {batch_index + 1} (ID: {batch_id}) - {batch_name}")
        print(f"   📊 任务数量: {len(tasks)}")

        # 获取并发配置
        execution_config = self.plan.get("execution_config", {})
        max_concurrent = execution_config.get("max_concurrent_requests", 2)

        # 创建任务列表
        task_coroutines = [
            self.execute_single_task(task, execution_config)
            for task in tasks
        ]

        # 并发执行（限制并发数）
        # 注意：由于通义万相API是异步任务+轮询，并发数不宜过高
        results = []
        for i in range(0, len(task_coroutines), max_concurrent):
            batch_coroutines = task_coroutines[i:i + max_concurrent]
            batch_results = await asyncio.gather(*batch_coroutines)
            results.extend(batch_results)

            # Checkpoint检查
            checkpoint_interval = execution_config.get("checkpoint_interval", 1)
            if (i + len(batch_coroutines)) % checkpoint_interval == 0:
                self.save_checkpoint()

        return results

    def save_checkpoint(self):
        """保存执行进度检查点"""
        output_config = self.plan.get("output_config", {})
        metadata_files = output_config.get("metadata_files", {})
        checkpoint_filename = metadata_files.get("checkpoint", "checkpoint.json")

        checkpoint_path = self.output_base / checkpoint_filename

        self.checkpoint_data["last_update"] = datetime.now().isoformat()
        self.checkpoint_data["completed_count"] = self.completed_tasks
        self.checkpoint_data["failed_count"] = self.failed_tasks

        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(self.checkpoint_data, f, ensure_ascii=False, indent=2)

        print(f"      💾 Checkpoint已保存: {checkpoint_path}")

    def generate_metadata(self):
        """生成执行元数据和交付清单"""
        print("\n📋 生成执行元数据...")

        output_config = self.plan.get("output_config", {})
        metadata_files = output_config.get("metadata_files", {})

        # 1. 执行日志
        execution_log_filename = metadata_files.get("execution_log", "execution-log.json")
        execution_log_path = self.output_base / execution_log_filename

        execution_log_data = {
            "plan_id": self.plan.get("plan_id"),
            "execution_time": datetime.now().isoformat(),
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": f"{(self.completed_tasks / self.total_tasks * 100):.2f}%" if self.total_tasks > 0 else "0%",
            "tasks": self.execution_log
        }

        with open(execution_log_path, 'w', encoding='utf-8') as f:
            json.dump(execution_log_data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ 执行日志: {execution_log_path}")

        # 2. E9交付清单
        delivery_manifest_filename = metadata_files.get("delivery_manifest", "delivery-manifest.yaml")
        e9_delivery_path = self.output_base / delivery_manifest_filename

        e9_delivery_data = {
            "plan_id": self.plan.get("plan_id"),
            "project_name": self.plan.get("project_name"),
            "delivery_time": datetime.now().isoformat(),
            "phase": "E8-图生视频完成（通义万相2.5）",
            "next_phase": "E9-配音生成（如需额外配音）",
            "statistics": {
                "total_videos": self.total_tasks,
                "generated_videos": self.completed_tasks,
                "failed_videos": self.failed_tasks
            },
            "output_directories": {
                "raw": str(self.output_subdirs["raw"]),
                "final": str(self.output_subdirs["final"]),
                "review": str(self.output_subdirs["review"]),
                "audio": str(self.output_subdirs.get("audio", ""))
            },
            "features_used": {
                "audio_modes": self._extract_audio_modes(),
                "video_effects": self._extract_video_effects()
            }
        }

        with open(e9_delivery_path, 'w', encoding='utf-8') as f:
            yaml.dump(e9_delivery_data, f, allow_unicode=True, sort_keys=False)
        print(f"   ✅ E9交付清单: {e9_delivery_path}")

    def _extract_audio_modes(self) -> List[str]:
        """提取使用的音频模式"""
        audio_modes = set()
        for batch in self.plan.get("batches", []):
            for task in batch.get("tasks", []):
                audio_config = task.get("parameters", {}).get("audio_config", {})
                if audio_config.get("enable_audio"):
                    audio_modes.add(audio_config.get("audio_mode", "auto_caption"))
                else:
                    audio_modes.add("silent")
        return list(audio_modes)

    def _extract_video_effects(self) -> List[str]:
        """提取使用的视频特效"""
        effects = set()
        for batch in self.plan.get("batches", []):
            for task in batch.get("tasks", []):
                effect_config = task.get("parameters", {}).get("effects", {})
                if effect_config.get("enable_effects"):
                    effects.add(effect_config.get("effect_type", "dynamic_light"))
        return list(effects)

    async def execute_plan(self):
        """执行完整计划"""
        print("\n" + "=" * 80)
        print("🚀 开始执行E8图生视频计划（通义万相2.5）")
        print("=" * 80)

        start_time = datetime.now()

        # 执行所有批次
        all_results = []
        for batch_index, batch in enumerate(self.plan.get("batches", [])):
            batch_results = await self.execute_batch(batch, batch_index)
            all_results.extend(batch_results)

            # 统计结果
            for result in batch_results:
                if result["success"]:
                    self.completed_tasks += 1
                    self.checkpoint_data["completed_task_ids"].append(result["task_id"])
                else:
                    self.failed_tasks += 1
                    self.checkpoint_data["failed_task_ids"].append(result["task_id"])

                self.execution_log.append(result)

        # 生成元数据
        self.generate_metadata()

        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        # 打印执行报告
        print("\n" + "=" * 80)
        print("📊 E8执行报告（通义万相2.5）")
        print("=" * 80)
        print(f"✅ 总任务数: {self.total_tasks}")
        print(f"✅ 成功生成: {self.completed_tasks}")
        print(f"❌ 失败任务: {self.failed_tasks}")
        print(f"📈 成功率: {(self.completed_tasks / self.total_tasks * 100):.2f}%" if self.total_tasks > 0 else "0%")
        print(f"⏱️  总耗时: {total_time:.2f}秒 ({total_time/60:.2f}分钟)")
        print(f"📁 输出目录: {self.output_base}")
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='执行E8图生视频计划（通义万相2.5）')
    parser.add_argument('--plan', required=True, help='执行计划JSON文件路径')

    args = parser.parse_args()

    # 创建执行引擎
    engine = E8ExecutionEngine(args.plan)

    # 加载计划
    if not engine.load_plan():
        sys.exit(1)

    # 验证输入
    if not engine.validate_input_files():
        print("\n⚠️  警告: 输入文件验证失败，但继续执行...")

    # 创建输出目录
    engine.setup_output_directories()

    # 执行计划
    try:
        asyncio.run(engine.execute_plan())
        print("\n🎉 E8执行计划完成！")
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        engine.save_checkpoint()
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ 执行异常: {e}")
        import traceback
        traceback.print_exc()
        engine.save_checkpoint()
        sys.exit(1)


if __name__ == "__main__":
    main()
