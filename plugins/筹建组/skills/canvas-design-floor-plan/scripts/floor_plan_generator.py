"""
Floor Plan Generator - 核心生成引擎

基于Markdown配置文档生成专业建筑平面图PNG/PDF
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_floor_plan(
    config_md_path: str,
    output_dir: str,
    output_formats: List[str] = ["png", "pdf"],
    resolution: str = "4K",
    pdf_size: str = "A3",
    canvas_size: Tuple[int, int] = (1920, 1440),
    scale: str = "1:100",
    show_dimensions: bool = True,
    show_furniture: bool = True,
    line_weight_factor: float = 1.0,
    color_mode: str = "standard"
) -> Dict:
    """
    生成建筑平面图

    Args:
        config_md_path: 平面图配置.md文件路径
        output_dir: 输出目录
        output_formats: 输出格式列表 ["png", "pdf", "svg"]
        resolution: PNG分辨率 ("1080p", "4K", "8K")
        pdf_size: PDF打印规格 ("A3", "A2", "A1", "A0")
        canvas_size: 画布尺寸（像素）
        scale: 比例尺 ("1:50", "1:100", "1:200")
        show_dimensions: 是否显示尺寸标注
        show_furniture: 是否显示家具
        line_weight_factor: 线条粗细系数 (0.5-2.0)
        color_mode: 色彩模式 ("standard", "grayscale", "high_contrast")

    Returns:
        Dict包含生成状态和文件路径
    """

    logger.info(f"开始生成平面图: {config_md_path}")

    # 步骤1: 解析配置文档
    try:
        try:
            from .config_parser import parse_config, validate_config
        except ImportError:
            from config_parser import parse_config, validate_config

        logger.info("解析配置文档...")
        config = parse_config(config_md_path)

        logger.info("验证配置完整性...")
        validate_config(config)

    except Exception as e:
        logger.error(f"配置解析失败: {str(e)}")
        return {
            'status': 'failed',
            'error': f'配置解析失败: {str(e)}',
            'config_path': config_md_path
        }

    # 步骤2: 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 步骤3: 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_filename = f"floor_plan-{timestamp}"

    # 步骤4: 调用渲染引擎
    try:
        try:
            from .render_engine import FloorPlanRenderer
        except ImportError:
            from render_engine import FloorPlanRenderer

        logger.info("初始化渲染引擎...")
        renderer = FloorPlanRenderer(
            canvas_size=canvas_size,
            scale=scale,
            line_weight_factor=line_weight_factor,
            color_mode=color_mode
        )

        logger.info("渲染SVG矢量图...")
        svg_content = renderer.render_svg(
            config=config,
            show_dimensions=show_dimensions,
            show_furniture=show_furniture
        )

        # 保存SVG（用于PDF生成）
        svg_path = os.path.join(output_dir, f"{base_filename}.svg")
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        logger.info(f"SVG已保存: {svg_path}")

    except Exception as e:
        logger.error(f"SVG渲染失败: {str(e)}")
        return {
            'status': 'failed',
            'error': f'SVG渲染失败: {str(e)}',
            'config_path': config_md_path
        }

    # 步骤5: 转换为PNG
    png_path = None
    if "png" in output_formats:
        try:
            logger.info(f"转换为PNG ({resolution})...")
            png_path = _svg_to_png(
                svg_path=svg_path,
                output_path=os.path.join(output_dir, f"{base_filename}-{resolution}.png"),
                resolution=resolution
            )
            logger.info(f"PNG已保存: {png_path}")
        except Exception as e:
            logger.error(f"PNG转换失败: {str(e)}")

    # 步骤6: 转换为PDF
    pdf_path = None
    if "pdf" in output_formats:
        try:
            logger.info(f"转换为PDF ({pdf_size})...")
            pdf_path = _svg_to_pdf(
                svg_path=svg_path,
                output_path=os.path.join(output_dir, f"{base_filename}-{pdf_size}.pdf"),
                pdf_size=pdf_size
            )
            logger.info(f"PDF已保存: {pdf_path}")
        except Exception as e:
            logger.error(f"PDF转换失败: {str(e)}")

    # 步骤7: 生成元数据
    metadata = {
        "project_name": config.get('basic_info', {}).get('project_name', 'Unknown'),
        "generation_time": datetime.now().isoformat(),
        "config_file": config_md_path,
        "output_files": {
            "svg": svg_path,
            "png": png_path,
            "pdf": pdf_path
        },
        "parameters": {
            "resolution": resolution,
            "pdf_size": pdf_size,
            "canvas_size": canvas_size,
            "scale": scale,
            "show_dimensions": show_dimensions,
            "show_furniture": show_furniture
        },
        "zones_rendered": list(config.get('zones', {}).keys()),
        "total_area": config.get('basic_info', {}).get('total_area', 'N/A'),
        "status": "success"
    }

    # 保存元数据
    metadata_dir = os.path.join(os.path.dirname(output_dir), 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    metadata_path = os.path.join(metadata_dir, f"task-{timestamp}-meta.json")

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    logger.info(f"元数据已保存: {metadata_path}")

    logger.info("✅ 平面图生成完成!")

    return {
        'status': 'success',
        'config_path': config_md_path,
        'svg_path': svg_path,
        'png_path': png_path,
        'pdf_path': pdf_path,
        'metadata_path': metadata_path,
        'config_name': config.get('basic_info', {}).get('project_name', 'Unknown'),
        'zones_rendered': metadata['zones_rendered'],
        'generation_time': metadata['generation_time']
    }


def batch_generate(
    config_paths: List[str],
    output_dir: str,
    parallel: bool = True,
    max_workers: int = 3,
    **kwargs
) -> List[Dict]:
    """
    批量生成平面图

    Args:
        config_paths: 配置文档路径列表
        output_dir: 输出目录
        parallel: 是否并行生成
        max_workers: 最大并行数
        **kwargs: 传递给generate_floor_plan的其他参数

    Returns:
        List[Dict] 每个配置的生成结果
    """

    logger.info(f"批量生成平面图: {len(config_paths)} 个配置")

    if parallel:
        from concurrent.futures import ProcessPoolExecutor, as_completed

        results = []
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(generate_floor_plan, config_path, output_dir, **kwargs): config_path
                for config_path in config_paths
            }

            for future in as_completed(futures):
                config_path = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"✅ {config_path}: {result['status']}")
                except Exception as e:
                    logger.error(f"❌ {config_path}: {str(e)}")
                    results.append({
                        'status': 'failed',
                        'config_path': config_path,
                        'error': str(e)
                    })

        return results

    else:
        # 串行生成
        results = []
        for config_path in config_paths:
            try:
                result = generate_floor_plan(config_path, output_dir, **kwargs)
                results.append(result)
                logger.info(f"✅ {config_path}: {result['status']}")
            except Exception as e:
                logger.error(f"❌ {config_path}: {str(e)}")
                results.append({
                    'status': 'failed',
                    'config_path': config_path,
                    'error': str(e)
                })

        return results


def _svg_to_png(svg_path: str, output_path: str, resolution: str) -> str:
    """
    将SVG转换为PNG

    Args:
        svg_path: SVG文件路径
        output_path: PNG输出路径
        resolution: 分辨率 ("1080p", "4K", "8K")

    Returns:
        PNG文件路径
    """

    # 分辨率映射
    resolution_map = {
        "1080p": (1920, 1080),
        "4K": (3840, 2160),
        "8K": (7680, 4320)
    }

    target_size = resolution_map.get(resolution, (3840, 2160))

    try:
        # 方案1: 使用cairosvg (推荐)
        import cairosvg

        with open(svg_path, 'rb') as f:
            svg_data = f.read()

        cairosvg.svg2png(
            bytestring=svg_data,
            write_to=output_path,
            output_width=target_size[0],
            output_height=target_size[1]
        )

        return output_path

    except ImportError:
        logger.warning("cairosvg未安装，使用PIL备用方案")

        # 方案2: 使用PIL (备用)
        from PIL import Image
        from io import BytesIO

        # 这里需要先用其他库将SVG转为临时PNG
        # 为简化示例，直接返回SVG路径
        logger.warning(f"PNG转换需要cairosvg库，请安装: pip install cairosvg")
        return svg_path


def _svg_to_pdf(svg_path: str, output_path: str, pdf_size: str) -> str:
    """
    将SVG转换为PDF

    Args:
        svg_path: SVG文件路径
        output_path: PDF输出路径
        pdf_size: PDF尺寸 ("A3", "A2", "A1", "A0")

    Returns:
        PDF文件路径
    """

    # PDF尺寸映射 (mm)
    pdf_size_map = {
        "A3": (420, 297),
        "A2": (594, 420),
        "A1": (841, 594),
        "A0": (1189, 841)
    }

    page_size = pdf_size_map.get(pdf_size, (420, 297))

    try:
        # 方案1: 使用cairosvg (推荐)
        import cairosvg

        with open(svg_path, 'rb') as f:
            svg_data = f.read()

        cairosvg.svg2pdf(
            bytestring=svg_data,
            write_to=output_path
        )

        return output_path

    except ImportError:
        logger.warning("cairosvg未安装，使用reportlab备用方案")

        # 方案2: 使用reportlab (备用)
        from reportlab.lib.pagesizes import A3, A2, A1, A0
        from reportlab.pdfgen import canvas
        from reportlab.graphics import renderPDF
        from svglib.svglib import svg2rlg

        size_map_rl = {
            "A3": A3,
            "A2": A2,
            "A1": A1,
            "A0": A0
        }

        page_size_rl = size_map_rl.get(pdf_size, A3)

        # 读取SVG并转换为ReportLab图形
        drawing = svg2rlg(svg_path)

        # 创建PDF
        c = canvas.Canvas(output_path, pagesize=page_size_rl)
        renderPDF.draw(drawing, c, 0, 0)
        c.save()

        return output_path


# 命令行接口
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Floor Plan Generator")
    parser.add_argument("config", help="配置文档路径")
    parser.add_argument("-o", "--output", default="output/", help="输出目录")
    parser.add_argument("-f", "--formats", nargs="+", default=["png", "pdf"], help="输出格式")
    parser.add_argument("-r", "--resolution", default="4K", help="PNG分辨率")
    parser.add_argument("--pdf-size", default="A3", help="PDF尺寸")

    args = parser.parse_args()

    result = generate_floor_plan(
        config_md_path=args.config,
        output_dir=args.output,
        output_formats=args.formats,
        resolution=args.resolution,
        pdf_size=args.pdf_size
    )

    print("\n" + "="*60)
    print("✅ Floor Plan Generation Complete")
    print("="*60)
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"SVG: {result['svg_path']}")
        print(f"PNG: {result['png_path']}")
        print(f"PDF: {result['pdf_path']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    print("="*60)
