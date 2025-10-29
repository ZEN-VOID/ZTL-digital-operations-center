"""
Integration Test - 集成测试脚本

测试完整的平面图生成流程
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# 直接导入同目录下的模块
from floor_plan_generator import generate_floor_plan


def test_basic_floor_plan():
    """测试基础平面图生成"""

    print("\n" + "="*60)
    print("测试1: 基础平面图生成（火锅店300㎡）")
    print("="*60)

    # 配置路径（相对于scripts目录）
    config_path = "../examples/example_hotpot_300sqm.md"

    # 输出目录（使用绝对路径）
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
    output_dir = os.path.join(project_root, "output/测试项目/Z1-平面图计划师/results/")

    # 执行生成
    try:
        result = generate_floor_plan(
            config_md_path=config_path,
            output_dir=output_dir,
            output_formats=["svg", "png", "pdf"],
            resolution="4K"
        )

        print("\n✅ 测试通过!")
        print(f"状态: {result['status']}")
        print(f"配置: {result['config_path']}")
        print(f"SVG: {result.get('svg_path', 'N/A')}")
        print(f"PNG: {result.get('png_path', 'N/A')}")
        print(f"PDF: {result.get('pdf_path', 'N/A')}")
        print(f"元数据: {result.get('metadata_path', 'N/A')}")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config_parser():
    """测试配置解析"""

    print("\n" + "="*60)
    print("测试2: 配置文档解析")
    print("="*60)

    from config_parser import parse_config, validate_config

    config_path = "../examples/example_hotpot_300sqm.md"

    try:
        # 解析配置
        config = parse_config(config_path)

        print(f"\n✅ 配置解析成功!")
        print(f"项目名称: {config['basic_info'].get('project_name', 'N/A')}")
        print(f"总面积: {config['basic_info'].get('total_area', 'N/A')}")
        print(f"功能分区数: {len(config['zones'])}")
        print(f"分区列表: {list(config['zones'].keys())}")

        # 验证配置
        validate_config(config)
        print("✅ 配置验证通过!")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_svg_rendering():
    """测试SVG渲染"""

    print("\n" + "="*60)
    print("测试3: SVG渲染引擎")
    print("="*60)

    from config_parser import parse_config
    from render_engine import FloorPlanRenderer

    config_path = "../examples/example_hotpot_300sqm.md"

    try:
        # 解析配置
        config = parse_config(config_path)

        # 初始化渲染器
        renderer = FloorPlanRenderer(
            canvas_size=(1920, 1440),
            scale="1:100",
            color_mode="standard"
        )

        # 渲染SVG
        svg_content = renderer.render_svg(config, show_dimensions=True, show_furniture=True)

        print(f"\n✅ SVG渲染成功!")
        print(f"SVG长度: {len(svg_content)} 字符")
        print(f"包含元素: {'<svg' in svg_content}, {'<rect' in svg_content}, {'<text' in svg_content}")

        # 保存SVG用于检查
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
        test_svg_path = os.path.join(project_root, "output/test_rendered.svg")
        os.makedirs(os.path.dirname(test_svg_path), exist_ok=True)
        with open(test_svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        print(f"测试SVG已保存: {test_svg_path}")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""

    print("\n" + "="*60)
    print("🧪 canvas-design-floor-plan 集成测试")
    print("="*60)

    results = []

    # 测试1: 配置解析
    results.append(("配置解析", test_config_parser()))

    # 测试2: SVG渲染
    results.append(("SVG渲染", test_svg_rendering()))

    # 测试3: 完整流程
    results.append(("完整流程", test_basic_floor_plan()))

    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")

        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n总计: {passed + failed} 个测试")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print("="*60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()

    if success:
        print("\n🎉 所有测试通过!")
        sys.exit(0)
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")
        sys.exit(1)
