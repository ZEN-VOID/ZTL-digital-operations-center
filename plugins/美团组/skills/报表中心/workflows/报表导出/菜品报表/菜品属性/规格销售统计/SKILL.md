---
name: 规格销售统计导出
description: 美团管家报表中心 - 菜品报表/菜品属性/规格销售统计 报表导出SOP
---

# 规格销售统计导出

## 🎯 功能概述

从美团管家报表中心导出规格销售统计数据。

**报表路径**: 菜品报表 > 菜品属性 > 规格销售统计

**直接访问URL**: [https://pos.meituan.com/web/report/main#/rms-report/规格销售](https://pos.meituan.com/web/report/main#/rms-report/规格销售)

## 📋 操作步骤

### 1. 访问报表页面

```
访问URL: https://pos.meituan.com/web/report/main#/rms-report/规格销售
等待页面加载完成
确认页面标题显示"规格销售统计"
```

### 2. 填写筛选条件


**1. 查询时间** (✅ 必填)
- 字段名: `time_range`
- 类型: `daterange`
- 说明: 选择报表统计的时间范围
- 操作: 点击日期选择器,选择起始日期和结束日期

**2. 门店选择** (✅ 必填)
- 字段名: `store_ids`
- 类型: `multiselect`
- 说明: 选择需要查询的门店
- 操作: 勾选需要查询的门店选择

**3. 属性类型** (⭕ 可选)
- 字段名: `attribute_type`
- 类型: `select`
- 可选值: 规格, 做法, 加料, 餐盒
- 操作: 从下拉菜单中选择属性类型

### 3. 查询数据

```
点击"查询"按钮
等待数据加载完成(通常1-5秒)
检查数据表格是否正确显示
确认数据条数和时间范围
```

### 4. 导出报表

```
点击"导出"或"下载"按钮
选择导出格式(Excel/CSV)
确认导出
等待下载完成(大数据量可能需要几分钟)
```

### 5. 验证导出结果

```
打开下载的Excel文件
检查数据完整性:
  - 表头字段是否完整
  - 数据行数是否正确
  - 数值计算是否准确
确认时间范围和筛选条件正确
```

## 🔧 Chrome MCP 自动化脚本

使用 chrome-mcp 工具自动化执行导出流程:

```javascript
// 1. 导航到报表页面
await chrome_navigate({
  url: "{url}",
  waitForSelector: ".report-container"
});


// 2. 填写查询时间
await chrome_click_element({
  selector: "[placeholder*='查询时间']"
});
await chrome_fill_form({
  fields: [
    {selector: "input[name='startDate']", value: "{{start_date}}" },
    {selector: "input[name='endDate']", value: "{{end_date}}" }
  ]
});

// 3. 选择门店选择
await chrome_click_element({
  selector: "[placeholder*='门店选择']"
});
// 勾选所有选项或指定选项
await chrome_click_element({
  selector: ".ant-select-dropdown .ant-checkbox-wrapper"
});

// 4. 选择属性类型
await chrome_click_element({
  selector: "[name='attribute_type']"
});
await chrome_click_element({
  textQuery: "{{selected_value}}"
});

// 5. 点击查询按钮
await chrome_click_element({
  selector: "button:has-text('查询')"
});

// 6. 等待数据加载
await chrome_wait_for({
  text: "查询成功",
  timeout: 30000
});

// 7. 点击导出按钮
await chrome_click_element({
  selector: "button:has-text('导出')"
});

// 8. 等待下载完成
await chrome_wait_for({
  text: "导出成功",
  timeout: 60000
});
```

## 📝 注意事项

### 权限要求
- ✅ 确保已登录美团管家系统
- ✅ 确保有权限访问该报表
- ✅ 确认账号具有数据导出权限

### 数据时效性
- ⚠️ 数据更新延迟: T+1天(建议查询前一天的数据)
- ⚠️ 跨天结账: 注意营业日的定义(结账时间决定营业日)
- ⚠️ 实时数据: 当天数据可能不完整

### 性能建议
- 💡 单次导出不超过3个月数据(避免超时)
- 💡 大数据量分批导出(按月/按周)
- 💡 避开营业高峰时段导出
- 💡 建议在营业结束后(22:00后)导出完整数据

### 常见问题
1. **导出超时**: 缩小时间范围或减少门店数量
2. **数据为空**: 检查时间范围和筛选条件
3. **数据不一致**: 等待数据同步完成后重新导出
4. **下载失败**: 检查浏览器下载设置和磁盘空间

## 🔗 相关文档

- [美团管家报表中心帮助文档](https://pos.meituan.com/web/report/main#/rms-report/help)
- [报表数据说明视频](https://h5.dianping.com/app/cs-faas-page/saas-mvp/video-list.html)
- [常见问题FAQ](https://h5.dianping.com/app/cs-faas-page/saas-mvp/video-list.html?id=2)

## 📊 字段说明


## 📈 数据用途

本报表数据可用于:

- ✅ 菜品销售分析
- ✅ 菜单优化决策
- ✅ 库存采购计划
- ✅ 定价策略调整

---

*本文档由 ZTL数智化作战中心 自动生成*
*最后更新: 2025-11-04*
