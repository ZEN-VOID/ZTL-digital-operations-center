#!/usr/bin/env python3
"""
Stage 1: Re-read Excel files with correct header parameter
Fix issue: 3.0 files have metadata in row 0, actual headers in row 1
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Define file paths
INPUT_DIR = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/input/情报组/【2.0 VS 3.0】产品销售对比")
OUTPUT_DIR = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/output/stage1-data-structure-analysis")

# File paths
file_2_0_baseline = INPUT_DIR / "客单价.xlsx"
file_3_0_order_details = INPUT_DIR / "吼巷_全渠道订单明细_20251027_0208_1761556082620.xlsx"
file_3_0_product_stats = INPUT_DIR / "吼巷_销售品项统计_2025-10-27_02_11_52_a899380r_1761556312749.xlsx"
file_3_0_business_overview = INPUT_DIR / "吼巷_营业概览_20251027_0143_a899380r_1761554593716.xlsx"

print("=" * 80)
print("Stage 1: Re-reading Excel files with correct header parameter")
print("=" * 80)

# Read files with correct header parameter
print("\n[1/4] Reading 2.0 baseline (header=0 - correct)...")
df_2_0 = pd.read_excel(file_2_0_baseline, header=0)
print(f"✓ Shape: {df_2_0.shape}")
print(f"✓ Columns: {list(df_2_0.columns[:5])}... ({len(df_2_0.columns)} total)")

print("\n[2/4] Reading 3.0 order details (header=1 - CORRECTED)...")
df_order_details = pd.read_excel(file_3_0_order_details, header=1)
print(f"✓ Shape: {df_order_details.shape}")
print(f"✓ Columns: {list(df_order_details.columns[:8])}...")
print(f"  Total columns: {len(df_order_details.columns)}")

print("\n[3/4] Reading 3.0 product stats (header=1 - CORRECTED)...")
df_product_stats = pd.read_excel(file_3_0_product_stats, header=1)
print(f"✓ Shape: {df_product_stats.shape}")
print(f"✓ Columns: {list(df_product_stats.columns)}")

print("\n[4/4] Reading 3.0 business overview (header=1 - CORRECTED)...")
df_business_overview = pd.read_excel(file_3_0_business_overview, header=1)
print(f"✓ Shape: {df_business_overview.shape}")
print(f"✓ Columns: {list(df_business_overview.columns)}")

# Generate corrected structure report
print("\n" + "=" * 80)
print("Generating corrected structure documentation...")
print("=" * 80)

def get_dataframe_info(df, name):
    """Extract comprehensive structure information from DataFrame"""
    info = {
        "file_name": name,
        "shape": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        },
        "columns": list(df.columns),
        "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_data": df.head(3).to_dict(orient='records'),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
    }
    return info

structure_report = {
    "report_metadata": {
        "generated_at": datetime.now().isoformat(),
        "description": "Corrected data structure analysis - 3.0 files re-read with header=1",
        "correction_reason": "3.0 files have metadata in row 0, actual headers in row 1"
    },
    "files": {
        "2.0_baseline": get_dataframe_info(df_2_0, "客单价.xlsx"),
        "3.0_order_details": get_dataframe_info(df_order_details, "吼巷_全渠道订单明细_20251027_0208_1761556082620.xlsx"),
        "3.0_product_stats": get_dataframe_info(df_product_stats, "吼巷_销售品项统计_2025-10-27_02_11_52_a899380r_1761556312749.xlsx"),
        "3.0_business_overview": get_dataframe_info(df_business_overview, "吼巷_营业概览_20251027_0143_a899380r_1761554593716.xlsx")
    }
}

# Save corrected structure report
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = OUTPUT_DIR / f"data-structure-report-corrected-{timestamp}.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(structure_report, f, ensure_ascii=False, indent=2)

print(f"\n✓ Corrected structure report saved: {output_file}")

# Display key corrections
print("\n" + "=" * 80)
print("KEY CORRECTIONS SUMMARY")
print("=" * 80)

print("\n[3.0 Order Details] Column names now properly extracted:")
print(f"  Before: Unnamed: 0, Unnamed: 1, Unnamed: 2...")
print(f"  After:  {', '.join(df_order_details.columns[:8])}...")

print("\n[3.0 Product Stats] Column names now properly extracted:")
print(f"  Before: 销售品项统计, Unnamed: 1, Unnamed: 2...")
print(f"  After:  {', '.join(df_product_stats.columns)}")

print("\n[3.0 Business Overview] Column names now properly extracted:")
print(f"  Before: 营业概览, Unnamed: 1, Unnamed: 2...")
print(f"  After:  {', '.join(df_business_overview.columns)}")

# Data quality validation
print("\n" + "=" * 80)
print("DATA QUALITY VALIDATION")
print("=" * 80)

print("\n[2.0 Baseline]")
print(f"  Missing values: {df_2_0.isnull().sum().sum()} cells")
print(f"  Memory usage: {structure_report['files']['2.0_baseline']['memory_usage_mb']} MB")

print("\n[3.0 Order Details]")
print(f"  Missing values: {df_order_details.isnull().sum().sum()} cells")
print(f"  Date range: {df_order_details['营业日期'].min() if '营业日期' in df_order_details.columns else 'N/A'} to {df_order_details['营业日期'].max() if '营业日期' in df_order_details.columns else 'N/A'}")
print(f"  Memory usage: {structure_report['files']['3.0_order_details']['memory_usage_mb']} MB")

print("\n[3.0 Product Stats]")
print(f"  Missing values: {df_product_stats.isnull().sum().sum()} cells")
print(f"  Memory usage: {structure_report['files']['3.0_product_stats']['memory_usage_mb']} MB")

print("\n[3.0 Business Overview]")
print(f"  Missing values: {df_business_overview.isnull().sum().sum()} cells")
print(f"  Memory usage: {structure_report['files']['3.0_business_overview']['memory_usage_mb']} MB")

print("\n" + "=" * 80)
print("✓ Stage 1 data structure analysis completed with corrections")
print(f"✓ Output: {output_file}")
print("=" * 80)
