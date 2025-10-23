# shadcn-ui MCP 技能包

---
name: shadcn-ui
description: shadcn/ui v4组件库集成，提供React组件源码、演示代码、元数据和区块(blocks)的检索能力，支持快速集成现代UI组件到项目中
---

## 快速开始

shadcn-ui是shadcn/ui v4组件库的MCP集成，提供了对shadcn/ui组件系统的完整访问能力。

### 基础用法

```python
# 1. 列出所有可用组件
components = await mcp__shadcn_ui__list_components()
print(f"可用组件: {', '.join(components)}")

# 2. 获取组件源代码
button_code = await mcp__shadcn_ui__get_component(
    componentName="button"
)

# 3. 获取组件演示代码
button_demo = await mcp__shadcn_ui__get_component_demo(
    componentName="button"
)

# 4. 获取组件元数据
button_meta = await mcp__shadcn_ui__get_component_metadata(
    componentName="button"
)
```

### 使用区块(Blocks)

```python
# 列出所有区块
blocks = await mcp__shadcn_ui__list_blocks()
# 或按类别筛选
calendar_blocks = await mcp__shadcn_ui__list_blocks(
    category="calendar"
)

# 获取区块源码
dashboard_block = await mcp__shadcn_ui__get_block(
    blockName="dashboard-01",
    includeComponents=True  # 包含依赖组件
)
```

---

## 核心能力

### 1. 组件检索

#### 列出所有组件
```python
# 获取完整组件列表
all_components = await mcp__shadcn_ui__list_components()

# 返回示例:
# ["accordion", "alert", "alert-dialog", "aspect-ratio", "avatar",
#  "badge", "button", "calendar", "card", "checkbox", ...]
```

#### 获取组件源码
```python
# 获取单个组件的完整源代码
accordion_source = await mcp__shadcn_ui__get_component(
    componentName="accordion"
)

# 返回内容包含:
# - TypeScript/React组件代码
# - 样式定义 (Tailwind CSS)
# - 类型定义
# - 导出声明
```

#### 获取组件演示
```python
# 获取组件的使用示例代码
accordion_demo = await mcp__shadcn_ui__get_component_demo(
    componentName="accordion"
)

# 返回内容:
# - 完整的React组件示例
# - 实际使用场景代码
# - 常见配置模式
```

#### 获取组件元数据
```python
# 获取组件的详细元信息
accordion_meta = await mcp__shadcn_ui__get_component_metadata(
    componentName="accordion"
)

# 返回信息包含:
# - 组件名称和描述
# - 依赖关系
# - 文件路径
# - 版本信息
```

### 2. 仓库结构

```python
# 获取shadcn-ui仓库的目录结构
structure = await mcp__shadcn_ui__get_directory_structure(
    owner="shadcn-ui",      # 默认值
    repo="ui",              # 默认值
    branch="main",          # 默认值
    path="apps/www/registry/default/ui"  # 默认v4 registry路径
)

# 自定义路径
blocks_structure = await mcp__shadcn_ui__get_directory_structure(
    path="apps/www/registry/default/block"
)
```

### 3. 区块(Blocks)系统

#### 列出所有区块
```python
# 获取所有区块
all_blocks = await mcp__shadcn_ui__list_blocks()

# 按类别筛选
calendar_blocks = await mcp__shadcn_ui__list_blocks(
    category="calendar"  # 可选: calendar, dashboard, login, sidebar, products
)

# 返回结构:
# {
#     "calendar": ["calendar-01", "calendar-02"],
#     "dashboard": ["dashboard-01", "dashboard-02", ...],
#     "login": ["login-01", "login-02", ...],
#     ...
# }
```

#### 获取区块源码
```python
# 获取简单区块 (单文件)
login_block = await mcp__shadcn_ui__get_block(
    blockName="login-01",
    includeComponents=False
)

# 获取复杂区块 (包含依赖组件)
dashboard_block = await mcp__shadcn_ui__get_block(
    blockName="dashboard-01",
    includeComponents=True  # 自动包含所有依赖组件文件
)

# 返回内容:
# {
#     "main": "主区块代码",
#     "components": {
#         "component1.tsx": "组件1代码",
#         "component2.tsx": "组件2代码"
#     }
# }
```

---

## 使用模式

### 模式1: 快速集成组件

**场景**: 需要在项目中快速添加shadcn/ui组件

```python
async def add_component_to_project(component_name: str, target_dir: str):
    """将shadcn/ui组件添加到项目中"""

    # 1. 获取组件源码
    source_code = await mcp__shadcn_ui__get_component(
        componentName=component_name
    )

    # 2. 获取使用示例
    demo_code = await mcp__shadcn_ui__get_component_demo(
        componentName=component_name
    )

    # 3. 保存到项目
    component_path = f"{target_dir}/components/ui/{component_name}.tsx"
    with open(component_path, 'w') as f:
        f.write(source_code)

    # 4. 创建示例文件
    example_path = f"{target_dir}/examples/{component_name}-example.tsx"
    with open(example_path, 'w') as f:
        f.write(demo_code)

    print(f"✅ 组件 {component_name} 已添加到项目")
    return component_path, example_path

# 使用示例
await add_component_to_project("button", "./src")
await add_component_to_project("card", "./src")
await add_component_to_project("dialog", "./src")
```

### 模式2: 批量导入组件

**场景**: 项目初始化时批量导入多个组件

```python
async def batch_import_components(components_list: list, target_dir: str):
    """批量导入shadcn/ui组件"""

    results = []

    for component_name in components_list:
        try:
            # 获取组件源码
            source = await mcp__shadcn_ui__get_component(
                componentName=component_name
            )

            # 保存组件
            path = f"{target_dir}/components/ui/{component_name}.tsx"
            with open(path, 'w') as f:
                f.write(source)

            results.append({
                "component": component_name,
                "status": "success",
                "path": path
            })

        except Exception as e:
            results.append({
                "component": component_name,
                "status": "failed",
                "error": str(e)
            })

    return results

# 批量导入常用组件
common_components = [
    "button", "card", "input", "label", "select",
    "dialog", "dropdown-menu", "table", "form", "toast"
]

import_results = await batch_import_components(
    components_list=common_components,
    target_dir="./src"
)

# 输出结果
success_count = sum(1 for r in import_results if r["status"] == "success")
print(f"✅ 成功导入 {success_count}/{len(common_components)} 个组件")
```

### 模式3: 使用区块快速搭建页面

**场景**: 使用预制区块快速搭建仪表板或登录页面

```python
async def scaffold_page_with_block(block_name: str, page_dir: str):
    """使用区块搭建页面"""

    # 1. 获取区块代码 (包含所有依赖组件)
    block_data = await mcp__shadcn_ui__get_block(
        blockName=block_name,
        includeComponents=True
    )

    # 2. 保存主区块文件
    main_path = f"{page_dir}/{block_name}.tsx"
    with open(main_path, 'w') as f:
        f.write(block_data["main"])

    # 3. 保存依赖组件 (如果有)
    component_paths = []
    if "components" in block_data:
        for comp_name, comp_code in block_data["components"].items():
            comp_path = f"{page_dir}/components/{comp_name}"
            os.makedirs(os.path.dirname(comp_path), exist_ok=True)
            with open(comp_path, 'w') as f:
                f.write(comp_code)
            component_paths.append(comp_path)

    print(f"✅ 区块 {block_name} 已创建")
    print(f"   主文件: {main_path}")
    print(f"   组件数: {len(component_paths)}")

    return {
        "main": main_path,
        "components": component_paths
    }

# 创建登录页面
await scaffold_page_with_block("login-01", "./src/pages/auth")

# 创建仪表板页面
await scaffold_page_with_block("dashboard-01", "./src/pages/dashboard")

# 创建日历页面
await scaffold_page_with_block("calendar-01", "./src/pages/calendar")
```

### 模式4: 组件探索与文档生成

**场景**: 为团队创建组件使用文档

```python
async def generate_component_docs(output_file: str):
    """生成shadcn/ui组件使用文档"""

    # 1. 获取所有组件列表
    components = await mcp__shadcn_ui__list_components()

    docs = ["# shadcn/ui 组件库文档\n\n"]

    # 2. 遍历每个组件
    for component_name in components:
        # 获取元数据
        meta = await mcp__shadcn_ui__get_component_metadata(
            componentName=component_name
        )

        # 获取演示代码
        demo = await mcp__shadcn_ui__get_component_demo(
            componentName=component_name
        )

        # 生成文档片段
        docs.append(f"## {component_name.title()}\n\n")
        docs.append(f"**路径**: `{meta.get('path', 'N/A')}`\n\n")
        docs.append(f"### 使用示例\n\n```tsx\n{demo}\n```\n\n")
        docs.append("---\n\n")

    # 3. 保存文档
    with open(output_file, 'w') as f:
        f.write(''.join(docs))

    print(f"✅ 组件文档已生成: {output_file}")
    print(f"   包含组件: {len(components)} 个")

# 生成文档
await generate_component_docs("./docs/shadcn-components.md")
```

---

## 最佳实践

### 1. 组件版本管理

```python
# ✅ 推荐: 在项目中记录使用的组件版本
async def track_component_versions(components_list: list):
    """记录组件版本信息"""

    version_info = {
        "shadcn-ui": "v4",
        "components": {}
    }

    for component_name in components_list:
        meta = await mcp__shadcn_ui__get_component_metadata(
            componentName=component_name
        )

        version_info["components"][component_name] = {
            "path": meta.get("path"),
            "imported_at": datetime.now().isoformat(),
            "version": meta.get("version", "v4")
        }

    # 保存版本信息
    with open("./components-version.json", 'w') as f:
        json.dump(version_info, f, indent=2)

    return version_info
```

### 2. 样式定制

```python
# shadcn/ui使用Tailwind CSS，建议在项目中配置主题
"""
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... 其他颜色
      },
    },
  },
}
"""
```

### 3. 组件组合

```python
# ✅ 推荐: 组合多个shadcn/ui组件创建复杂UI
async def create_composite_component(component_names: list, target_file: str):
    """组合多个组件创建复杂UI"""

    imports = []
    components_code = []

    for name in component_names:
        source = await mcp__shadcn_ui__get_component(componentName=name)
        components_code.append(source)
        imports.append(f'import {{ {name.title()} }} from "@/components/ui/{name}"')

    # 创建组合组件模板
    composite = f"""
{chr(10).join(imports)}

export function CompositeComponent() {{
  return (
    <div className="composite-component">
      {{/* 在这里组合使用导入的组件 */}}
    </div>
  )
}}
"""

    with open(target_file, 'w') as f:
        f.write(composite)

    return target_file
```

### 4. 依赖检查

```python
# ✅ 推荐: 检查组件依赖关系
async def check_component_dependencies(component_name: str):
    """检查组件的依赖关系"""

    meta = await mcp__shadcn_ui__get_component_metadata(
        componentName=component_name
    )

    source = await mcp__shadcn_ui__get_component(
        componentName=component_name
    )

    # 分析源码中的import语句
    imports = re.findall(r'from ["\']@/components/ui/([^"\']+)["\']', source)

    print(f"组件 {component_name} 的依赖:")
    for dep in imports:
        print(f"  - {dep}")

    return imports
```

---

## 常见问题

### 1. 组件不存在

**问题**: 获取组件时返回错误

```python
# ❌ 错误示例
try:
    component = await mcp__shadcn_ui__get_component(
        componentName="nonexistent-component"
    )
except Exception as e:
    print(f"组件不存在: {e}")

# ✅ 正确做法: 先列出可用组件
available = await mcp__shadcn_ui__list_components()
if "button" in available:
    button = await mcp__shadcn_ui__get_component(componentName="button")
```

### 2. 区块依赖处理

**问题**: 复杂区块包含多个文件

```python
# ✅ 使用includeComponents参数
block = await mcp__shadcn_ui__get_block(
    blockName="dashboard-01",
    includeComponents=True  # 自动包含所有依赖
)

# 处理返回的多文件结构
if isinstance(block, dict):
    # 主文件
    main_code = block.get("main", "")

    # 依赖组件
    components = block.get("components", {})
    for filename, code in components.items():
        print(f"组件文件: {filename}")
```

### 3. TypeScript类型定义

**问题**: 需要类型定义文件

```python
# shadcn/ui组件已包含TypeScript类型
# 确保项目配置支持TypeScript

"""
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
"""
```

### 4. 样式不生效

**问题**: 组件样式没有正确加载

**解决方案**:
1. 确保安装了Tailwind CSS
2. 配置了CSS变量 (在全局CSS中)
3. 导入了组件样式

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    /* ... 其他CSS变量 */
  }
}
```

---

## 集成示例

### 示例1: Next.js项目集成

```python
import os
import asyncio

async def setup_shadcn_in_nextjs(project_root: str):
    """在Next.js项目中设置shadcn/ui"""

    # 1. 创建组件目录
    ui_dir = f"{project_root}/src/components/ui"
    os.makedirs(ui_dir, exist_ok=True)

    # 2. 导入基础组件
    base_components = [
        "button", "input", "card", "label",
        "select", "dialog", "dropdown-menu"
    ]

    for comp in base_components:
        source = await mcp__shadcn_ui__get_component(componentName=comp)

        comp_path = f"{ui_dir}/{comp}.tsx"
        with open(comp_path, 'w') as f:
            f.write(source)

        print(f"✅ 导入组件: {comp}")

    # 3. 创建utils文件 (cn辅助函数)
    utils_content = '''
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''

    utils_path = f"{project_root}/src/lib/utils.ts"
    os.makedirs(os.path.dirname(utils_path), exist_ok=True)
    with open(utils_path, 'w') as f:
        f.write(utils_content)

    print("\n🎉 shadcn/ui设置完成!")
    print(f"   组件位置: {ui_dir}")
    print(f"   工具函数: {utils_path}")

# 运行设置
await setup_shadcn_in_nextjs("./my-nextjs-app")
```

### 示例2: 创建表单页面

```python
async def create_form_page(output_dir: str):
    """使用shadcn/ui组件创建表单页面"""

    # 1. 导入表单相关组件
    form_components = ["form", "input", "label", "button", "card"]

    for comp in form_components:
        source = await mcp__shadcn_ui__get_component(componentName=comp)

        comp_path = f"{output_dir}/components/ui/{comp}.tsx"
        os.makedirs(os.path.dirname(comp_path), exist_ok=True)
        with open(comp_path, 'w') as f:
            f.write(source)

    # 2. 创建表单页面
    form_page = '''
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function ContactForm() {
  return (
    <Card className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">联系我们</h2>

      <form className="space-y-4">
        <div>
          <Label htmlFor="name">姓名</Label>
          <Input id="name" placeholder="请输入您的姓名" />
        </div>

        <div>
          <Label htmlFor="email">邮箱</Label>
          <Input id="email" type="email" placeholder="your@email.com" />
        </div>

        <div>
          <Label htmlFor="message">留言</Label>
          <Input id="message" placeholder="请输入留言内容" />
        </div>

        <Button type="submit" className="w-full">
          提交
        </Button>
      </form>
    </Card>
  )
}
'''

    page_path = f"{output_dir}/pages/contact.tsx"
    os.makedirs(os.path.dirname(page_path), exist_ok=True)
    with open(page_path, 'w') as f:
        f.write(form_page)

    print(f"✅ 表单页面已创建: {page_path}")

await create_form_page("./src")
```

### 示例3: 探索和测试所有区块

```python
async def explore_all_blocks(output_dir: str):
    """探索并保存所有shadcn/ui区块"""

    # 1. 获取所有区块
    all_blocks = await mcp__shadcn_ui__list_blocks()

    # 2. 创建探索报告
    report = ["# shadcn/ui Blocks 探索报告\n\n"]

    for category, block_names in all_blocks.items():
        report.append(f"## {category.title()} 类别\n\n")

        for block_name in block_names:
            # 获取区块代码
            block_data = await mcp__shadcn_ui__get_block(
                blockName=block_name,
                includeComponents=True
            )

            # 保存区块文件
            block_dir = f"{output_dir}/blocks/{category}/{block_name}"
            os.makedirs(block_dir, exist_ok=True)

            # 保存主文件
            with open(f"{block_dir}/main.tsx", 'w') as f:
                f.write(block_data.get("main", ""))

            # 保存组件文件
            if "components" in block_data:
                comp_dir = f"{block_dir}/components"
                os.makedirs(comp_dir, exist_ok=True)

                for comp_name, comp_code in block_data["components"].items():
                    with open(f"{comp_dir}/{comp_name}", 'w') as f:
                        f.write(comp_code)

            # 添加到报告
            comp_count = len(block_data.get("components", {}))
            report.append(f"- **{block_name}**: {comp_count} 个组件文件\n")

        report.append("\n")

    # 3. 保存报告
    with open(f"{output_dir}/blocks-report.md", 'w') as f:
        f.write(''.join(report))

    print(f"✅ 区块探索完成: {output_dir}/blocks/")
    print(f"📄 探索报告: {output_dir}/blocks-report.md")

await explore_all_blocks("./shadcn-exploration")
```

---

## 提示与技巧

### 1. 快速原型开发

使用区块快速创建原型页面，而不是从零开始:

```python
# 快速创建管理后台原型
await scaffold_page_with_block("dashboard-01", "./prototype/admin")
await scaffold_page_with_block("sidebar-01", "./prototype/admin")
```

### 2. 组件定制

shadcn/ui组件可以直接修改源码进行定制:

```python
# 1. 导入组件
source = await mcp__shadcn_ui__get_component(componentName="button")

# 2. 修改样式或逻辑
customized = source.replace(
    'className="...',
    'className="custom-styles ...'
)

# 3. 保存定制版本
with open("./components/ui/custom-button.tsx", 'w') as f:
    f.write(customized)
```

### 3. 团队协作

创建组件使用指南帮助团队成员:

```python
# 为每个导入的组件生成使用示例
for component in ["button", "card", "dialog"]:
    demo = await mcp__shadcn_ui__get_component_demo(componentName=component)

    with open(f"./docs/components/{component}.md", 'w') as f:
        f.write(f"# {component.title()} 组件使用指南\n\n")
        f.write(f"```tsx\n{demo}\n```\n")
```

### 4. 性能优化

使用代码分割和懒加载减少初始包大小:

```tsx
// 使用React.lazy懒加载shadcn/ui组件
import { lazy } from 'react'

const Dialog = lazy(() => import('@/components/ui/dialog'))
const Calendar = lazy(() => import('@/components/ui/calendar'))
```

### 5. 主题切换

利用CSS变量实现深色/浅色主题:

```css
/* 浅色主题 */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
}

/* 深色主题 */
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

---

## 相关资源

- **官方文档**: https://ui.shadcn.com
- **GitHub仓库**: https://github.com/shadcn-ui/ui
- **组件演示**: https://ui.shadcn.com/docs/components
- **区块展示**: https://ui.shadcn.com/blocks
- **Tailwind CSS**: https://tailwindcss.com
- **Radix UI**: https://www.radix-ui.com (shadcn/ui基于Radix UI构建)

---

**技能包版本**: 1.0.0
**shadcn/ui版本**: v4
**更新时间**: 2025-10-23
**维护状态**: ✅ 活跃维护
