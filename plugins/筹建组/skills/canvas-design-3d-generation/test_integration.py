#!/usr/bin/env python3
"""
canvas-design-3d-generation 技能包集成测试
验证Z3-3D生成AIGC助手的完整性

测试维度:
1. 目录结构完整性
2. SKILL.md格式和元数据
3. 配置模板格式验证
4. API客户端导入测试
5. Z3智能体定义验证
6. 输出路径规范检查
"""

import sys
from pathlib import Path
import json
import re

# 添加项目根目录到Python路径
# From: .../plugins/筹建组/skills/canvas-design-3d-generation/test_integration.py
# To: .../ZTL数智化作战中心/
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name: str, passed: bool, message: str = ""):
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if message:
        print(f"     {Colors.YELLOW}{message}{Colors.END}")
    return passed

def test_directory_structure():
    """测试1: 目录结构完整性"""
    skill_root = Path(__file__).parent

    required_files = [
        "SKILL.md",
        "README.md",
        "scripts/api_client.py",
        "scripts/config_template.json"
    ]

    required_dirs = [
        "scripts"
    ]

    missing_files = [f for f in required_files if not (skill_root / f).exists()]
    missing_dirs = [d for d in required_dirs if not (skill_root / d).is_dir()]

    if missing_files or missing_dirs:
        message = f"缺失文件: {missing_files}, 缺失目录: {missing_dirs}"
        return print_test("目录结构完整性", False, message)

    return print_test("目录结构完整性", True, "所有必需文件和目录存在")

def test_skill_md_format():
    """测试2: SKILL.md格式验证"""
    skill_md = Path(__file__).parent / "SKILL.md"

    if not skill_md.exists():
        return print_test("SKILL.md格式", False, "文件不存在")

    content = skill_md.read_text(encoding='utf-8')

    # 检查YAML frontmatter
    if not content.startswith('---'):
        return print_test("SKILL.md格式", False, "缺少YAML frontmatter")

    # 检查必需字段
    required_fields = ['name:', 'description:']
    missing_fields = [f for f in required_fields if f not in content]

    if missing_fields:
        return print_test("SKILL.md格式", False, f"缺少字段: {missing_fields}")

    # 检查核心章节
    required_sections = [
        '## 🎯 核心能力',
        '## 🚀 快速开始',
        '## 🛠️ 使用脚本'
    ]

    missing_sections = [s for s in required_sections if s not in content]

    if missing_sections:
        return print_test("SKILL.md格式", False, f"缺少章节: {missing_sections}")

    # 检查TripoSR关键词
    if 'triposr' not in content.lower():
        return print_test("SKILL.md格式", False, "未提及TripoSR技术")

    return print_test("SKILL.md格式", True, "格式完整,包含所有必需章节")

def test_config_template():
    """测试3: 配置模板格式验证"""
    config_file = Path(__file__).parent / "scripts" / "config_template.json"

    if not config_file.exists():
        return print_test("配置模板格式", False, "config_template.json不存在")

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return print_test("配置模板格式", False, f"JSON格式错误: {e}")

    # 检查必需顶层字段
    required_top_fields = [
        'project_info',
        'generation_config',
        'scenes_to_generate'
    ]

    missing_fields = [f for f in required_top_fields if f not in config]
    if missing_fields:
        return print_test("配置模板格式", False, f"缺少字段: {missing_fields}")

    # 检查generation_config
    gen_config = config.get('generation_config', {})
    if gen_config.get('model') != 'triposr':
        return print_test("配置模板格式", False, "model应为'triposr'")

    # 检查scenes_to_generate
    scenes = config.get('scenes_to_generate', [])
    if not scenes:
        return print_test("配置模板格式", False, "scenes_to_generate为空")

    # 检查第一个场景的必需字段
    scene = scenes[0]
    required_scene_fields = [
        'scene_id',
        'scene_name',
        'input_image',
        'parameters',
        'output_path'
    ]

    missing_scene_fields = [f for f in required_scene_fields if f not in scene]
    if missing_scene_fields:
        return print_test("配置模板格式", False, f"场景缺少字段: {missing_scene_fields}")

    # 检查parameters
    params = scene.get('parameters', {})
    if params.get('format') not in ['glb', 'obj', 'fbx']:
        return print_test("配置模板格式", False, "format应为glb/obj/fbx之一")

    return print_test("配置模板格式", True, f"配置有效,包含{len(scenes)}个场景")

def test_api_client_import():
    """测试4: API客户端导入测试"""
    api_client_file = Path(__file__).parent / "scripts" / "api_client.py"

    if not api_client_file.exists():
        return print_test("API客户端导入", False, "api_client.py不存在")

    content = api_client_file.read_text(encoding='utf-8')

    # 检查关键类定义
    if 'class TripoSRClient' not in content:
        return print_test("API客户端导入", False, "未定义TripoSRClient类")

    # 检查关键方法
    required_methods = [
        'def generate_3d_model',
        'def batch_generate'
    ]

    missing_methods = [m for m in required_methods if m not in content]
    if missing_methods:
        return print_test("API客户端导入", False, f"缺少方法: {missing_methods}")

    # 检查API endpoint配置
    if 'replicate' not in content.lower():
        return print_test("API客户端导入", False, "未配置Replicate API")

    # 检查命令行入口
    if 'def main()' not in content:
        return print_test("API客户端导入", False, "缺少命令行入口main()")

    # 检查argparse子命令
    if 'subparsers' not in content:
        return print_test("API客户端导入", False, "缺少子命令支持")

    return print_test("API客户端导入", True, "TripoSRClient类定义完整,支持单张和批量生成")

def test_agent_definition():
    """测试5: Z3智能体定义验证"""
    agent_file = project_root / "plugins" / "筹建组" / "agents" / "Z3-3D生成AIGC助手.md"

    if not agent_file.exists():
        return print_test("Z3智能体定义", False, "Z3-3D生成AIGC助手.md不存在")

    content = agent_file.read_text(encoding='utf-8')

    # 检查YAML frontmatter
    if not content.startswith('---'):
        return print_test("Z3智能体定义", False, "缺少YAML frontmatter")

    # 检查核心章节 (Z3的实际结构)
    required_sections = [
        '## 1. 身份定位',
        '## 2. 核心技术能力',
        '## 3. 6-Step AIGC工作流',
        '## 模型列表'
    ]

    missing_sections = [s for s in required_sections if s not in content]
    if missing_sections:
        return print_test("Z3智能体定义", False, f"缺少章节: {missing_sections}")

    # 检查TripoSR技术栈
    if 'triposr' not in content.lower():
        return print_test("Z3智能体定义", False, "未提及TripoSR技术")

    # 检查技能包引用
    if 'canvas-design-3d-generation' not in content:
        return print_test("Z3智能体定义", False, "未引用canvas-design-3d-generation技能包")

    # 检查输出格式
    output_formats = ['glb', 'obj', 'fbx']
    found_formats = [fmt for fmt in output_formats if fmt.upper() in content or fmt.lower() in content]
    if len(found_formats) < 2:
        return print_test("Z3智能体定义", False, "支持的3D格式不足")

    # 检查成本估算
    if '$' not in content or '成本' not in content:
        return print_test("Z3智能体定义", False, "缺少成本估算信息")

    return print_test("Z3智能体定义", True, f"智能体定义完整,支持{len(found_formats)}种3D格式")

def test_output_path_convention():
    """测试6: 输出路径规范检查"""
    config_file = Path(__file__).parent / "scripts" / "config_template.json"

    if not config_file.exists():
        return print_test("输出路径规范", False, "config_template.json不存在")

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 检查output_config
    output_config = config.get('output_config', {})
    if not output_config:
        return print_test("输出路径规范", False, "缺少output_config配置")

    base_dir = output_config.get('base_dir', '')

    # 检查路径格式: output/[项目名]/Z3-3D生成AIGC助手
    expected_pattern = r'output/.+/Z3-3D生成AIGC助手'
    if not re.search(expected_pattern, base_dir):
        return print_test("输出路径规范", False, f"路径格式不符合规范: {base_dir}")

    # 检查场景输出路径
    scenes = config.get('scenes_to_generate', [])
    if scenes:
        scene = scenes[0]
        output_path = scene.get('output_path', '')

        # 检查是否包含Z3-3D生成AIGC助手
        if 'Z3-3D生成AIGC助手' not in output_path:
            return print_test("输出路径规范", False, "场景输出路径未包含智能体名称")

        # 检查文件扩展名
        if not any(output_path.endswith(ext) for ext in ['.glb', '.obj', '.fbx']):
            return print_test("输出路径规范", False, "输出路径缺少有效的3D格式扩展名")

    return print_test("输出路径规范", True, "输出路径符合全局规范")

def main():
    """运行所有测试"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}canvas-design-3d-generation 技能包集成测试{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

    tests = [
        ("目录结构完整性", test_directory_structure),
        ("SKILL.md格式", test_skill_md_format),
        ("配置模板格式", test_config_template),
        ("API客户端导入", test_api_client_import),
        ("Z3智能体定义", test_agent_definition),
        ("输出路径规范", test_output_path_convention)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print_test(test_name, False, f"异常: {str(e)}")
            results.append(False)
        print()  # 空行分隔

    # 统计
    passed = sum(results)
    total = len(results)
    pass_rate = (passed / total * 100) if total > 0 else 0

    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}测试结果汇总{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

    if passed == total:
        print(f"{Colors.GREEN}✅ 所有测试通过!{Colors.END}")
    else:
        print(f"{Colors.RED}❌ 部分测试失败{Colors.END}")

    print(f"\n通过率: {Colors.GREEN if pass_rate == 100 else Colors.RED}{passed}/{total} ({pass_rate:.1f}%){Colors.END}")

    # 检查项详情
    print(f"\n{Colors.BLUE}检查项详情:{Colors.END}")
    for i, (test_name, _) in enumerate(tests, 1):
        status = "✅" if results[i-1] else "❌"
        print(f"  {status} {i}. {test_name}")

    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}\n")

    # 返回退出码
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
