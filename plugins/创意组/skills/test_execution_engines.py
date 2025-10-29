#!/usr/bin/env python3
"""
X4 Execution Engines Test Suite
================================
Validates the three newly added execution engines:
1. canvas_engine.py (canvas-design-restaurant)
2. p5js_executor.py (algorithmic-art-restaurant)
3. theme_applier.py (theme-factory-restaurant)

Usage:
    python test_execution_engines.py --all
    python test_execution_engines.py --canvas
    python test_execution_engines.py --p5js
    python test_execution_engines.py --theme
"""

import sys
from pathlib import Path

# Add skill directories to Python path
canvas_dir = Path(__file__).parent / "canvas-design-restaurant" / "scripts"
p5js_dir = Path(__file__).parent / "algorithmic-art-restaurant" / "scripts"
theme_dir = Path(__file__).parent / "theme-factory-restaurant" / "scripts"

sys.path.insert(0, str(canvas_dir))
sys.path.insert(0, str(p5js_dir))
sys.path.insert(0, str(theme_dir))

# Import execution engines
from canvas_engine import create_poster, create_menu_cover, create_packaging
from p5js_executor import generate_pattern
from theme_applier import apply_preset_theme, list_available_themes


# ============================================
# Test Cases
# ============================================

def test_canvas_engine():
    """Test canvas-design-restaurant execution engine"""
    print("\n" + "="*60)
    print("🎨 Testing Canvas Design Engine")
    print("="*60 + "\n")

    # Test 1: Poster Design
    print("📋 Test 1: Poster Design Brief Generation")
    print("-" * 60)
    result = create_poster(
        content="火锅店开业庆典,全场8折优惠,2025年1月28日盛大开业",
        cuisine_type="hotpot",
        dimensions="1920x1080",
        style="modern",
        project_name="执行引擎测试-海报"
    )

    if result["success"]:
        print(f"✅ Poster brief generated successfully!")
        print(f"   📁 Brief: {result['brief_path']}")
        print(f"   📋 Metadata: {result['metadata_path']}")
    else:
        print(f"❌ Failed: {result.get('error')}")

    # Test 2: Menu Cover Design
    print("\n📋 Test 2: Menu Cover Design Brief Generation")
    print("-" * 60)
    result = create_menu_cover(
        restaurant_name="蜀香火锅",
        cuisine_type="hotpot",
        style="elegant",
        project_name="执行引擎测试-菜单"
    )

    if result["success"]:
        print(f"✅ Menu cover brief generated successfully!")
        print(f"   📁 Brief: {result['brief_path']}")
    else:
        print(f"❌ Failed: {result.get('error')}")

    # Test 3: Packaging Design
    print("\n📋 Test 3: Packaging Design Brief Generation")
    print("-" * 60)
    result = create_packaging(
        item_type="外卖盒",
        cuisine_type="chinese",
        pattern_style="geometric",
        project_name="执行引擎测试-包装"
    )

    if result["success"]:
        print(f"✅ Packaging brief generated successfully!")
        print(f"   📁 Brief: {result['brief_path']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def test_p5js_executor():
    """Test algorithmic-art-restaurant execution engine"""
    print("\n" + "="*60)
    print("🎭 Testing P5.js Pattern Generator")
    print("="*60 + "\n")

    pattern_types = ["flowfield", "particles", "geometric", "noise"]

    for i, pattern_type in enumerate(pattern_types, 1):
        print(f"📋 Test {i}: {pattern_type.capitalize()} Pattern")
        print("-" * 60)

        result = generate_pattern(
            pattern_type=pattern_type,
            cuisine_type="chinese",
            seed=12345,
            width=1920,
            height=1080,
            project_name=f"执行引擎测试-算法艺术"
        )

        if result["success"]:
            print(f"✅ {pattern_type.capitalize()} pattern generated successfully!")
            print(f"   📁 Sketch: {result['sketch_path']}")
            print(f"   📋 Metadata: {result['metadata_path']}")
            print(f"   💡 Expected output: {result['expected_filename']}")
        else:
            print(f"❌ Failed: {result.get('error')}")

        print()


def test_theme_applier():
    """Test theme-factory-restaurant execution engine"""
    print("\n" + "="*60)
    print("🎨 Testing Theme Factory Engine")
    print("="*60 + "\n")

    # Test 1: List Available Themes
    print("📋 Test 1: List Available Themes")
    print("-" * 60)
    themes = list_available_themes()
    print(f"✅ Found {len(themes)} themes:")
    for theme_id, theme_name in themes.items():
        print(f"   • {theme_id:25s} - {theme_name}")

    # Test 2-4: Apply Different Themes
    test_themes = [
        ("chinese-imperial", "中式火锅店"),
        ("japanese-zen", "日式料理店"),
        ("cafe-moderne", "现代咖啡馆")
    ]

    for i, (theme_id, project_name) in enumerate(test_themes, 2):
        print(f"\n📋 Test {i}: Apply {theme_id} Theme")
        print("-" * 60)

        result = apply_preset_theme(
            theme_id=theme_id,
            project_name=f"执行引擎测试-{project_name}"
        )

        if result["success"]:
            print(f"✅ Theme '{result['theme_name']}' applied successfully!")
            print(f"   📁 CSS: {result['css_path']}")
            print(f"   📋 Metadata: {result['metadata_path']}")
            print(f"   📖 Guide: {result['guide_path']}")
        else:
            print(f"❌ Failed: {result.get('error')}")


def test_integration_workflow():
    """Test integrated workflow using all three engines"""
    print("\n" + "="*60)
    print("🔗 Testing Integrated Workflow")
    print("="*60 + "\n")

    project_name = "执行引擎测试-完整工作流"

    print("步骤 1: 应用主题 (Theme Factory)")
    print("-" * 60)
    theme_result = apply_preset_theme(
        theme_id="hotpot-fiesta",
        project_name=project_name
    )
    if theme_result["success"]:
        print(f"✅ Theme applied: {theme_result['theme_name']}")
        theme_colors = theme_result['theme']['colors']
        print(f"   Primary color: {theme_colors['primary']}")
        print(f"   Secondary color: {theme_colors['secondary']}")

    print("\n步骤 2: 生成算法图案 (Algorithmic Art)")
    print("-" * 60)
    pattern_result = generate_pattern(
        pattern_type="flowfield",
        cuisine_type="hotpot",
        seed=54321,
        width=1920,
        height=1080,
        project_name=project_name
    )
    if pattern_result["success"]:
        print(f"✅ Pattern generated: {pattern_result['sketch_path']}")

    print("\n步骤 3: 创建海报设计 (Canvas Design)")
    print("-" * 60)
    poster_result = create_poster(
        content="火锅盛宴,全场五折,今日开业",
        cuisine_type="hotpot",
        dimensions="2:3",
        style="energetic",
        project_name=project_name
    )
    if poster_result["success"]:
        print(f"✅ Poster brief created: {poster_result['brief_path']}")

    print("\n" + "="*60)
    print("✅ Integrated workflow completed!")
    print("="*60)
    print(f"\nAll outputs saved to: output/{project_name}/X4-平面设计师/")
    print("\n下一步:")
    print("1. 在 p5.js editor 中运行生成的 flowfield 图案代码")
    print("2. 使用生成的主题 CSS 变量")
    print("3. 根据 poster brief 在 Figma/Canvas 中创建最终海报")
    print("4. 整合图案、主题和海报为完整设计交付物")


def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*60)
    print("🚀 X4 Execution Engines Test Suite")
    print("="*60)
    print("\nTesting 3 execution engines:")
    print("  1. canvas_engine.py")
    print("  2. p5js_executor.py")
    print("  3. theme_applier.py")

    test_canvas_engine()
    test_p5js_executor()
    test_theme_applier()
    test_integration_workflow()

    print("\n" + "="*60)
    print("🎉 All Tests Completed!")
    print("="*60)
    print("\n检查 output/ 目录查看所有生成的文件")


# ============================================
# CLI Interface
# ============================================

def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="X4 Execution Engines Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_execution_engines.py --all          # Run all tests
  python test_execution_engines.py --canvas       # Test canvas engine only
  python test_execution_engines.py --p5js         # Test p5.js executor only
  python test_execution_engines.py --theme        # Test theme applier only
  python test_execution_engines.py --integration  # Test integrated workflow
        """
    )

    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--canvas", action="store_true", help="Test canvas engine")
    parser.add_argument("--p5js", action="store_true", help="Test p5.js executor")
    parser.add_argument("--theme", action="store_true", help="Test theme applier")
    parser.add_argument("--integration", action="store_true", help="Test integrated workflow")

    args = parser.parse_args()

    # If no arguments, default to --all
    if not any([args.all, args.canvas, args.p5js, args.theme, args.integration]):
        args.all = True

    try:
        if args.all:
            run_all_tests()
        else:
            if args.canvas:
                test_canvas_engine()
            if args.p5js:
                test_p5js_executor()
            if args.theme:
                test_theme_applier()
            if args.integration:
                test_integration_workflow()

        print("\n✅ Test suite executed successfully!")
        return 0

    except Exception as e:
        print(f"\n❌ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
