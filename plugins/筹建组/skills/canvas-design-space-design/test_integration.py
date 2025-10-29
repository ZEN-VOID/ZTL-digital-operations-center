#!/usr/bin/env python3
"""
Canvas Design - Space Design 集成测试脚本

测试项:
1. 技能包目录结构完整性
2. 配置文件格式正确性
3. API客户端可导入性
4. 示例配置文件验证
"""

import os
import json
import sys
from pathlib import Path

# 添加scripts目录到路径
skill_root = Path(__file__).parent
scripts_dir = skill_root / "scripts"
sys.path.insert(0, str(scripts_dir))

class Colors:
    """终端颜色输出"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test(test_name: str):
    """打印测试名称"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}[测试] {test_name}{Colors.END}")

def print_success(message: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message: str):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def test_directory_structure():
    """测试1: 验证目录结构完整性"""
    print_test("测试1: 目录结构完整性")

    required_files = [
        "SKILL.md",
        "README.md",
        "scripts/api_client.py",
        "scripts/config_template.json",
        "examples/hotpot-300sqm-new-chinese.json"
    ]

    all_pass = True
    for file_path in required_files:
        full_path = skill_root / file_path
        if full_path.exists():
            print_success(f"{file_path} 存在")
        else:
            print_error(f"{file_path} 缺失")
            all_pass = False

    return all_pass

def test_skill_md_format():
    """测试2: 验证SKILL.md格式"""
    print_test("测试2: SKILL.md格式验证")

    skill_md_path = skill_root / "SKILL.md"

    if not skill_md_path.exists():
        print_error("SKILL.md文件不存在")
        return False

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查YAML frontmatter
    if content.startswith('---'):
        print_success("包含YAML frontmatter")

        # 解析YAML
        yaml_end = content.find('---', 3)
        if yaml_end > 0:
            yaml_content = content[3:yaml_end]

            if 'name:' in yaml_content:
                print_success("包含name字段")
            else:
                print_error("缺少name字段")
                return False

            if 'description:' in yaml_content:
                print_success("包含description字段")
            else:
                print_error("缺少description字段")
                return False
        else:
            print_error("YAML frontmatter格式错误")
            return False
    else:
        print_error("缺少YAML frontmatter")
        return False

    # 检查核心章节
    required_sections = [
        "# 空间设计效果图生成",
        "## 🎯 核心能力",
        "## 🚀 快速开始",
        "## 🎨 设计风格库"
    ]

    for section in required_sections:
        if section in content:
            print_success(f"包含章节: {section}")
        else:
            print_warning(f"缺少建议章节: {section}")

    return True

def test_config_template():
    """测试3: 验证配置模板JSON格式"""
    print_test("测试3: 配置模板JSON格式验证")

    config_path = skill_root / "scripts" / "config_template.json"

    if not config_path.exists():
        print_error("config_template.json不存在")
        return False

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        print_success("JSON格式正确")

        # 检查必需字段
        required_fields = [
            "project_info",
            "design_positioning",
            "space_scenes",
            "execution_config",
            "api_config"
        ]

        all_present = True
        for field in required_fields:
            if field in config:
                print_success(f"包含字段: {field}")
            else:
                print_error(f"缺少字段: {field}")
                all_present = False

        # 验证space_scenes结构
        if "space_scenes" in config and len(config["space_scenes"]) > 0:
            scene = config["space_scenes"][0]
            scene_fields = ["scene_name", "prompt", "generation_params"]

            for field in scene_fields:
                if field in scene:
                    print_success(f"space_scenes包含字段: {field}")
                else:
                    print_error(f"space_scenes缺少字段: {field}")
                    all_present = False

        return all_present

    except json.JSONDecodeError as e:
        print_error(f"JSON解析失败: {e}")
        return False

def test_example_config():
    """测试4: 验证示例配置文件"""
    print_test("测试4: 示例配置文件验证")

    example_path = skill_root / "examples" / "hotpot-300sqm-new-chinese.json"

    if not example_path.exists():
        print_error("示例配置文件不存在")
        return False

    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        print_success("示例配置JSON格式正确")

        # 验证场景数量
        scenes = config.get("space_scenes", [])
        scene_count = len(scenes)
        print_success(f"包含 {scene_count} 个空间场景")

        if scene_count >= 5:
            print_success("场景数量合理(≥5)")
        else:
            print_warning(f"场景数量较少({scene_count}),建议至少5个场景")

        # 验证Prompt质量
        for idx, scene in enumerate(scenes, 1):
            prompt = scene.get("prompt", "")
            prompt_length = len(prompt)

            if prompt_length >= 200:
                print_success(f"场景{idx} '{scene.get('scene_name')}': Prompt长度合格({prompt_length}字符)")
            else:
                print_warning(f"场景{idx} '{scene.get('scene_name')}': Prompt较短({prompt_length}字符)")

            # 检查8要素
            elements_check = {
                "空间类型": any(word in prompt.lower() for word in ["restaurant", "hotpot", "entrance", "dining", "room"]),
                "风格": any(word in prompt.lower() for word in ["chinese", "style", "modern", "traditional"]),
                "材料": any(word in prompt.lower() for word in ["wood", "metal", "glass", "stone", "concrete"]),
                "照明": any(word in prompt.lower() for word in ["lighting", "light", "bright", "warm", "soft"]),
                "质量标签": any(word in prompt.lower() for word in ["8k", "photographic", "quality", "rendering"])
            }

            missing_elements = [elem for elem, present in elements_check.items() if not present]
            if not missing_elements:
                print_success(f"  场景{idx}: Prompt包含核心要素")
            else:
                print_warning(f"  场景{idx}: 可能缺少要素: {', '.join(missing_elements)}")

        return True

    except json.JSONDecodeError as e:
        print_error(f"示例配置JSON解析失败: {e}")
        return False

def test_api_client_import():
    """测试5: API客户端可导入性"""
    print_test("测试5: API客户端导入测试")

    try:
        import api_client
        print_success("api_client模块导入成功")

        # 检查核心类
        if hasattr(api_client, 'StableDiffusionXLClient'):
            print_success("StableDiffusionXLClient类存在")

            # 检查核心方法
            client_class = api_client.StableDiffusionXLClient
            required_methods = ['generate_image', 'generate_batch']

            for method in required_methods:
                if hasattr(client_class, method):
                    print_success(f"方法存在: {method}")
                else:
                    print_error(f"方法缺失: {method}")
                    return False

            return True
        else:
            print_error("StableDiffusionXLClient类不存在")
            return False

    except ImportError as e:
        print_error(f"导入失败: {e}")
        return False
    except Exception as e:
        print_error(f"导入测试失败: {e}")
        return False

def test_agent_definition():
    """测试6: Z2智能体定义验证"""
    print_test("测试6: Z2智能体定义验证")

    agent_path = skill_root.parent.parent / "agents" / "Z2-空间设计师.md"

    if not agent_path.exists():
        print_warning("Z2-空间设计师.md不存在(可能尚未提交)")
        return True  # 不算作失败

    with open(agent_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否提到canvas-design-space-design
    if "canvas-design-space-design" in content:
        print_success("Agent定义引用了正确的技能包名称")
    else:
        print_warning("Agent定义可能需要更新技能包引用")

    # 检查6-step workflow
    if "6-step" in content.lower() or "六步" in content:
        print_success("包含6步工作流")
    else:
        print_warning("可能缺少6步工作流定义")

    return True

def main():
    """主测试流程"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Canvas Design - Space Design 集成测试{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

    tests = [
        ("目录结构完整性", test_directory_structure),
        ("SKILL.md格式", test_skill_md_format),
        ("配置模板格式", test_config_template),
        ("示例配置文件", test_example_config),
        ("API客户端导入", test_api_client_import),
        ("Z2智能体定义", test_agent_definition)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"测试异常: {e}")
            results.append((test_name, False))

    # 汇总结果
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}测试结果汇总{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"{status}  {test_name}")

    print(f"\n{Colors.BOLD}总计: {passed}/{total} 测试通过{Colors.END}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ 所有测试通过! canvas-design-space-design技能包已就绪{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ {total - passed} 个测试失败,请修复后重试{Colors.END}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
