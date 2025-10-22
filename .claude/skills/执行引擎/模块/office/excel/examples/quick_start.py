"""
Excel自动化处理 - 快速开始示例

展示Excel Skill的基本使用方法
"""

from pathlib import Path
import sys

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from excel_processor import ExcelProcessor
from excel_reporter import ExcelReporter, DEFAULT_STYLES


def example_1_basic_read_write():
    """示例1: 基础读写操作"""
    print("\n=== 示例1: 基础读写操作 ===")

    processor = ExcelProcessor()

    # 创建示例数据
    import pandas as pd
    data = pd.DataFrame({
        '门店': ['门店A', '门店B', '门店C'],
        '销售额': [10000, 15000, 12000],
        '订单数': [100, 150, 120]
    })

    # 写入Excel到项目根目录的output/行政组/excel/目录
    output_path = 'output/行政组/excel/example1_basic.xlsx'
    processor.write(data, output_path)
    print(f"✓ 数据已写入: {output_path}")

    # 读取Excel
    read_data = processor.read(output_path)
    print(f"✓ 读取数据形状: {read_data.shape}")
    print(read_data)


def example_2_data_cleaning():
    """示例2: 数据清洗"""
    print("\n=== 示例2: 数据清洗 ===")

    import pandas as pd
    import numpy as np

    processor = ExcelProcessor()

    # 创建包含脏数据的示例
    dirty_data = pd.DataFrame({
        '日期': ['2025-01-01', '2025-01-02', None, '2025-01-04'],
        '门店': ['门店A', '门店B', '门店A', '门店B'],
        '销售额': [1000, None, 1500, 2000],
        '订单数': [10, 15, 12, 20]
    })

    print("清洗前:")
    print(dirty_data)

    # 数据清洗
    cleaned = processor.clean_data(dirty_data, {
        'fill_na': 0,  # 用0填充空值
        'remove_duplicates': False,
        'convert_types': {
            '日期': 'datetime',
            '销售额': 'float'
        }
    })

    print("\n清洗后:")
    print(cleaned)

    # 保存
    processor.write(cleaned, 'output/行政组/excel/example2_cleaned.xlsx')
    print("\n✓ 清洗后数据已保存")


def example_3_group_analysis():
    """示例3: 分组分析"""
    print("\n=== 示例3: 分组分析 ===")

    import pandas as pd

    processor = ExcelProcessor()

    # 创建销售数据
    sales_data = pd.DataFrame({
        '日期': pd.date_range('2025-01-01', periods=12, freq='D'),
        '门店': ['门店A', '门店B', '门店C'] * 4,
        '产品': ['产品1', '产品1', '产品2', '产品2', '产品1', '产品2'] * 2,
        '销售额': [1000, 1500, 1200, 1800, 1100, 1600,
                  1300, 1700, 1400, 1900, 1200, 1500],
        '销量': [10, 15, 12, 18, 11, 16, 13, 17, 14, 19, 12, 15]
    })

    # 按门店分组统计
    store_summary = processor.group_by(
        sales_data,
        group_cols=['门店'],
        agg_cols={'销售额': 'sum', '销量': 'sum', '日期': 'count'}
    )

    print("门店汇总:")
    print(store_summary)

    # 保存
    processor.write({
        '原始数据': sales_data,
        '门店汇总': store_summary
    }, 'output/战略组/销售分析/example3_analysis.xlsx')
    print("\n✓ 分析结果已保存")


def example_4_generate_report():
    """示例4: 生成带图表的报表"""
    print("\n=== 示例4: 生成带图表的报表 ===")

    import pandas as pd

    processor = ExcelProcessor()
    reporter = ExcelReporter()

    # 创建月度数据
    monthly_data = pd.DataFrame({
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '销售额': [50000, 55000, 60000, 58000, 62000, 65000],
        '成本': [30000, 32000, 35000, 34000, 36000, 38000],
        '利润': [20000, 23000, 25000, 24000, 26000, 27000]
    })

    # 创建报表
    output_path = 'output/战略组/reports/example4_report.xlsx'
    reporter.create_report(
        data=monthly_data,
        output=output_path,
        config={
            'title': '2025年上半年经营报表',
            'charts': [
                {
                    'type': 'line',
                    'x': '月份',
                    'y': '销售额',
                    'position': 'E2',
                    'title': '销售额趋势'
                },
                {
                    'type': 'bar',
                    'x': '月份',
                    'y': '利润',
                    'position': 'E15',
                    'title': '利润对比'
                }
            ],
            'styles': DEFAULT_STYLES
        }
    )

    print(f"✓ 报表已生成: {output_path}")


def example_5_batch_processing():
    """示例5: 批量处理"""
    print("\n=== 示例5: 批量处理 ===")

    import pandas as pd
    from pathlib import Path

    processor = ExcelProcessor()

    # 准备测试数据目录
    test_dir = Path('output/中台组/batch_test')
    test_dir.mkdir(parents=True, exist_ok=True)

    # 创建多个测试文件
    for i in range(3):
        data = pd.DataFrame({
            '门店': [f'门店{chr(65+i)}'] * 5,
            '日期': pd.date_range('2025-01-01', periods=5, freq='D'),
            '销售额': [1000 + i*100 + j*50 for j in range(5)]
        })
        processor.write(data, test_dir / f'store_{chr(65+i)}.xlsx')

    print(f"✓ 已创建 3 个测试文件")

    # 批量合并
    merged = processor.merge_files(
        pattern=str(test_dir / '*.xlsx'),
        output='output/中台组/数据汇总/example5_merged.xlsx'
    )

    print(f"✓ 合并完成，共 {len(merged)} 行数据")
    print(merged.head())


def main():
    """运行所有示例"""
    # 创建输出目录（相对于项目根目录）
    output_dirs = [
        'output/行政组/excel',
        'output/战略组/销售分析',
        'output/战略组/reports',
        'output/中台组/batch_test',
        'output/中台组/数据汇总'
    ]
    for dir_path in output_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Excel自动化处理 - 快速开始示例")
    print("=" * 60)

    try:
        example_1_basic_read_write()
        example_2_data_cleaning()
        example_3_group_analysis()
        example_4_generate_report()
        example_5_batch_processing()

        print("\n" + "=" * 60)
        print("✓ 所有示例运行完成！")
        print("查看 output/ 目录下的生成文件")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
