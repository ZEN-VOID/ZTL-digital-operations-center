#!/bin/bash
# 批量分析4张吼巷IP形象图片
# 使用E3智能体的标准化执行流程

echo "=================================================="
echo "吼巷IP形象批量分析 - E3智能体"
echo "=================================================="
echo ""

# 定义4个图片路径
images=(
  "input/吼巷/设计/IP/微信图片_20250923171141_52_171.png"
  "input/吼巷/设计/IP/微信图片_20250923171142_53_171.png"
  "input/吼巷/设计/IP/微信图片_20250923171157_55_171.jpg"
  "input/吼巷/设计/IP/微信图片_20250923171305_56_171.png"
)

# 循环处理每张图片
for i in "${!images[@]}"; do
  image_num=$((i + 1))
  image_path="${images[$i]}"

  echo "[$image_num/4] 分析图片: $image_path"

  # 生成临时任务JSON
  task_json="api/plans/e3-image-recognition/temp-task-$image_num.json"

  cat > "$task_json" << EOF
{
  "agent_id": "E3",
  "task_description": "吼巷品牌IP形象图片${image_num}专业分析",
  "input_data": {
    "image_url": "$image_path",
    "analysis_type": "comprehensive",
    "analysis_dimensions": [
      "视觉特征识别",
      "整体设计分析",
      "场景与应用评估",
      "商业价值洞察",
      "专业建议"
    ]
  },
  "output_settings": {
    "save_path": "output/analysis/e3-image-recognition/houthang-ip/",
    "format": "json"
  },
  "metadata": {
    "created_at": "$(date +%Y-%m-%dT%H:%M:%S)",
    "created_by": "E3批量分析脚本",
    "version": "1.0",
    "notes": "吼巷品牌IP形象${image_num}深度分析"
  }
}
EOF

  # 执行分析
  python api/projects/nano-banana-api/execute_plan.py --plan "$task_json"

  # 清理临时文件
  rm "$task_json"

  echo ""
  echo "[$image_num/4] 完成"
  echo ""

  # 间隔5秒避免API限流
  if [ $image_num -lt 4 ]; then
    echo "等待5秒..."
    sleep 5
  fi
done

echo "=================================================="
echo "✅ 批量分析完成！共处理4张图片"
echo "=================================================="
