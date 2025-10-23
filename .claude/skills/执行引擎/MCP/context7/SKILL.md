---
name: context7
description: Real-time library documentation retrieval with resolve-library-id and get-library-docs. Use for fetching up-to-date API docs, code examples, and library information when working with any framework or package.
---

# Context7 Skill

基于context7-mcp的实时库文档检索能力包，提供两步式文档获取流程：库名称解析 → 文档检索。

## Quick Start

### 基础使用

```python
# 1. 解析库名称获取Library ID
library_info = await resolve_library_id(libraryName="react")

# 2. 获取库文档
docs = await get_library_docs(
    context7CompatibleLibraryID=library_info['id'],
    topic="hooks",
    tokens=5000
)

print(docs)
```

### 快速查询流程

```python
# Step 1: 查找React文档
react_id = await resolve_library_id(libraryName="react")

# Step 2: 获取hooks相关文档
hooks_docs = await get_library_docs(
    context7CompatibleLibraryID=react_id['id'],
    topic="hooks"
)
```

## Core Capabilities

### 1. 库名称解析 (resolve-library-id)

**功能**: 将包/产品名称转换为Context7兼容的库ID

**使用场景**:
- 不知道确切的Library ID格式时
- 需要搜索匹配的库时
- 验证库是否被Context7支持时

**参数**:
```python
libraryName: str  # 库名称，如 "react", "next.js", "vue"
```

**返回格式**:
```python
{
    "id": "/vercel/next.js",           # Context7兼容的库ID
    "name": "Next.js",                 # 库名称
    "description": "The React Framework",  # 描述
    "trust_score": 9,                  # 信任分数 (0-10)
    "code_snippets": 1250              # 代码片段数量
}
```

#### 使用示例

```python
# 示例1: 查找React
react = await resolve_library_id(libraryName="react")
# 返回: {"id": "/facebook/react", "name": "React", ...}

# 示例2: 查找Next.js
nextjs = await resolve_library_id(libraryName="next.js")
# 返回: {"id": "/vercel/next.js", "name": "Next.js", ...}

# 示例3: 查找MongoDB
mongodb = await resolve_library_id(libraryName="mongodb")
# 返回: {"id": "/mongodb/docs", "name": "MongoDB", ...}

# 示例4: 查找Supabase
supabase = await resolve_library_id(libraryName="supabase")
# 返回: {"id": "/supabase/supabase", "name": "Supabase", ...}
```

#### 选择逻辑

Context7会根据以下优先级选择最佳匹配：

1. **名称相似度**: 精确匹配优先
2. **描述相关性**: 与查询意图的匹配度
3. **文档覆盖率**: Code Snippet数量越多越优先
4. **信任分数**: Trust Score 7-10的库更权威

**最佳实践**:

```python
# ✓ 推荐：使用官方包名
await resolve_library_id(libraryName="next.js")

# ✓ 可接受：使用产品名
await resolve_library_id(libraryName="Next.js")

# ✗ 避免：使用不明确的缩写
await resolve_library_id(libraryName="njs")
```

### 2. 获取库文档 (get-library-docs)

**功能**: 获取指定库的最新文档和代码示例

**使用场景**:
- 查询API参考文档
- 获取使用示例
- 学习框架特性

**参数**:
```python
context7CompatibleLibraryID: str  # 必需，从resolve-library-id获取
topic: str                        # 可选，聚焦主题如"hooks", "routing"
tokens: int                       # 可选，文档token限制，默认5000
```

**返回格式**:
```python
{
    "library_id": "/vercel/next.js",
    "topic": "routing",
    "documentation": """
        # Next.js Routing

        Next.js has a file-system based router...

        ## App Router (app directory)

        ```typescript
        // app/page.tsx
        export default function Page() {
          return <h1>Hello, Next.js!</h1>
        }
        ```

        ## Dynamic Routes

        ...
    """,
    "tokens_used": 3542
}
```

#### 使用示例

##### 基础查询

```python
# 1. 获取React完整文档（默认5000 tokens）
react_id = await resolve_library_id(libraryName="react")
react_docs = await get_library_docs(
    context7CompatibleLibraryID=react_id['id']
)

# 2. 获取Next.js路由文档
nextjs_id = await resolve_library_id(libraryName="next.js")
routing_docs = await get_library_docs(
    context7CompatibleLibraryID=nextjs_id['id'],
    topic="routing"
)

# 3. 获取Tailwind CSS配置文档
tailwind_id = await resolve_library_id(libraryName="tailwind css")
config_docs = await get_library_docs(
    context7CompatibleLibraryID=tailwind_id['id'],
    topic="configuration"
)
```

##### 控制文档长度

```python
# 获取更多上下文（10000 tokens）
detailed_docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js",
    topic="data fetching",
    tokens=10000
)

# 获取简洁摘要（2000 tokens）
summary_docs = await get_library_docs(
    context7CompatibleLibraryID="/mongodb/docs",
    topic="queries",
    tokens=2000
)
```

##### 主题聚焦

```python
# React Hooks文档
hooks_docs = await get_library_docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks"
)

# Vue Composition API文档
composition_docs = await get_library_docs(
    context7CompatibleLibraryID="/vuejs/vue",
    topic="composition api"
)

# Express中间件文档
middleware_docs = await get_library_docs(
    context7CompatibleLibraryID="/expressjs/express",
    topic="middleware"
)
```

#### 直接使用Library ID

如果你已知Library ID格式（`/org/project`或`/org/project/version`），可跳过resolve步骤：

```python
# 使用已知Library ID
docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js",
    topic="api routes"
)

# 使用特定版本
v14_docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js/v14.3.0-canary.87",
    topic="app router"
)
```

## Usage Patterns

### Pattern 1: 学习新框架

```python
async def learn_framework(framework_name: str, topics: list):
    """学习框架的多个主题"""

    # 1. 解析库ID
    lib = await resolve_library_id(libraryName=framework_name)
    print(f"📚 学习 {lib['name']}")
    print(f"   文档覆盖: {lib['code_snippets']} 代码片段")
    print(f"   信任分数: {lib['trust_score']}/10\n")

    # 2. 获取各主题文档
    docs_collection = {}
    for topic in topics:
        print(f"📖 获取主题: {topic}")
        docs = await get_library_docs(
            context7CompatibleLibraryID=lib['id'],
            topic=topic,
            tokens=5000
        )
        docs_collection[topic] = docs
        print(f"   ✓ {docs['tokens_used']} tokens\n")

    return docs_collection

# 使用示例
docs = await learn_framework(
    framework_name="next.js",
    topics=["routing", "data fetching", "api routes", "middleware"]
)
```

### Pattern 2: API参考查询

```python
async def query_api_reference(library: str, api_name: str):
    """查询特定API的参考文档"""

    # 1. 解析库
    lib = await resolve_library_id(libraryName=library)

    # 2. 获取API文档
    docs = await get_library_docs(
        context7CompatibleLibraryID=lib['id'],
        topic=api_name,
        tokens=3000
    )

    # 3. 提取代码示例
    code_examples = extract_code_blocks(docs['documentation'])

    return {
        "library": lib['name'],
        "api": api_name,
        "documentation": docs['documentation'],
        "examples": code_examples
    }

# 使用示例
useState_ref = await query_api_reference(
    library="react",
    api_name="useState"
)
```

### Pattern 3: 多库对比

```python
async def compare_libraries(libraries: list, topic: str):
    """对比多个库的同一主题实现"""

    comparisons = {}

    for lib_name in libraries:
        # 解析库
        lib = await resolve_library_id(libraryName=lib_name)

        # 获取主题文档
        docs = await get_library_docs(
            context7CompatibleLibraryID=lib['id'],
            topic=topic,
            tokens=3000
        )

        comparisons[lib['name']] = {
            "documentation": docs['documentation'],
            "trust_score": lib['trust_score'],
            "coverage": lib['code_snippets']
        }

    return comparisons

# 使用示例: 对比React和Vue的状态管理
comparison = await compare_libraries(
    libraries=["react", "vue", "svelte"],
    topic="state management"
)
```

### Pattern 4: 版本文档查询

```python
async def get_versioned_docs(library: str, version: str, topic: str):
    """获取特定版本的文档"""

    # 1. 构建版本化Library ID
    lib = await resolve_library_id(libraryName=library)
    base_id = lib['id']
    versioned_id = f"{base_id}/{version}"

    # 2. 获取版本文档
    docs = await get_library_docs(
        context7CompatibleLibraryID=versioned_id,
        topic=topic
    )

    return docs

# 使用示例
next14_docs = await get_versioned_docs(
    library="next.js",
    version="v14.3.0-canary.87",
    topic="app router"
)
```

### Pattern 5: 文档缓存优化

```python
class DocsCache:
    """文档缓存管理"""

    def __init__(self):
        self.cache = {}

    async def get_docs(self, library: str, topic: str = None):
        """获取文档（带缓存）"""

        cache_key = f"{library}:{topic or 'default'}"

        # 检查缓存
        if cache_key in self.cache:
            print(f"📦 从缓存获取: {cache_key}")
            return self.cache[cache_key]

        # 获取新文档
        print(f"🌐 从Context7获取: {cache_key}")
        lib = await resolve_library_id(libraryName=library)
        docs = await get_library_docs(
            context7CompatibleLibraryID=lib['id'],
            topic=topic
        )

        # 缓存
        self.cache[cache_key] = docs
        return docs

# 使用示例
cache = DocsCache()
react_hooks = await cache.get_docs("react", "hooks")
react_hooks_again = await cache.get_docs("react", "hooks")  # 从缓存
```

## Best Practices

### 1. 优先使用resolve-library-id

```python
# ✓ 推荐：先解析，再获取文档
lib = await resolve_library_id(libraryName="react")
docs = await get_library_docs(context7CompatibleLibraryID=lib['id'])

# ✗ 不推荐：猜测Library ID格式
docs = await get_library_docs(context7CompatibleLibraryID="/react/react")
```

**原因**: resolve-library-id会返回最权威的匹配，避免ID格式错误

### 2. 使用topic参数聚焦内容

```python
# ✓ 推荐：指定topic获取精准内容
docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js",
    topic="routing"
)

# ✗ 不推荐：获取全部文档后自己筛选
all_docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js",
    tokens=20000
)
# 然后手动搜索routing相关内容...
```

**原因**: topic参数让Context7智能聚焦，节省tokens

### 3. 控制tokens避免超限

```python
# ✓ 推荐：根据需要设置合理的token限制
quick_ref = await get_library_docs(
    context7CompatibleLibraryID="/mongodb/docs",
    topic="queries",
    tokens=2000  # 简洁参考
)

# ✓ 深度学习时增加tokens
detailed_guide = await get_library_docs(
    context7CompatibleLibraryID="/mongodb/docs",
    topic="aggregation",
    tokens=8000  # 详细教程
)

# ✗ 避免：盲目请求大量tokens
docs = await get_library_docs(
    context7CompatibleLibraryID="/react/react",
    tokens=50000  # 可能超出限制或浪费
)
```

### 4. 检查trust_score和coverage

```python
# ✓ 推荐：选择高质量库
lib = await resolve_library_id(libraryName="react state management")

if lib['trust_score'] >= 7 and lib['code_snippets'] > 100:
    docs = await get_library_docs(context7CompatibleLibraryID=lib['id'])
else:
    print(f"⚠️  库质量较低: Trust={lib['trust_score']}, Snippets={lib['code_snippets']}")
    # 考虑使用其他库或补充其他文档源
```

### 5. 使用明确的主题关键词

```python
# ✓ 推荐：使用官方术语
docs = await get_library_docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="useEffect"  # 官方hook名称
)

# ✓ 可接受：使用概念性关键词
docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js",
    topic="server components"  # Next.js官方概念
)

# ✗ 避免：使用模糊或非标准术语
docs = await get_library_docs(
    context7CompatibleLibraryID="/react/react",
    topic="那个生命周期的东西"  # 不明确
)
```

## Common Issues

### Issue 1: 库名称解析失败

**症状**: `resolve_library_id`返回空或不匹配

**原因**:
- 库名称拼写错误
- Context7未收录该库
- 使用了非官方名称

**解决方案**:
```python
# 1. 尝试不同名称变体
names = ["next.js", "nextjs", "Next.js", "vercel/next.js"]
for name in names:
    try:
        lib = await resolve_library_id(libraryName=name)
        print(f"✓ 找到: {lib['name']}")
        break
    except:
        continue

# 2. 使用更通用的关键词
lib = await resolve_library_id(libraryName="react framework")

# 3. 如果确定Library ID，直接使用
docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js"
)
```

### Issue 2: 文档内容不全

**症状**: 返回的文档缺少预期内容

**原因**:
- tokens限制过低
- topic关键词不准确
- 库的文档覆盖不完整

**解决方案**:
```python
# 1. 增加tokens限制
docs = await get_library_docs(
    context7CompatibleLibraryID="/mongodb/docs",
    topic="aggregation",
    tokens=10000  # 从5000增加到10000
)

# 2. 尝试更精确的topic
docs = await get_library_docs(
    context7CompatibleLibraryID="/react/react",
    topic="useEffect cleanup"  # 更具体
)

# 3. 不使用topic获取完整文档
docs = await get_library_docs(
    context7CompatibleLibraryID="/supabase/supabase",
    tokens=15000
)
```

### Issue 3: 版本不匹配

**症状**: 获取的文档与使用的库版本不符

**原因**:
- 未指定版本，获取的是最新版文档
- 版本号格式不正确

**解决方案**:
```python
# 1. 使用版本化Library ID
docs = await get_library_docs(
    context7CompatibleLibraryID="/vercel/next.js/v14.3.0-canary.87",
    topic="app router"
)

# 2. 在topic中包含版本信息
docs = await get_library_docs(
    context7CompatibleLibraryID="/react/react",
    topic="React 18 hooks"
)

# 3. 检查库的版本覆盖
lib = await resolve_library_id(libraryName="next.js")
print(f"描述: {lib['description']}")  # 可能包含版本信息
```

## Integration Examples

### Example 1: 与Agents集成

```python
# 智能体使用context7辅助代码生成
class CodeGeneratorAgent:
    async def generate_component(self, framework: str, component_type: str):
        """生成框架组件"""

        # 1. 获取框架文档
        lib = await resolve_library_id(libraryName=framework)
        docs = await get_library_docs(
            context7CompatibleLibraryID=lib['id'],
            topic=component_type
        )

        # 2. 基于文档生成代码
        code = self.generate_from_docs(docs['documentation'])

        return code

# 使用
agent = CodeGeneratorAgent()
button_code = await agent.generate_component("react", "button component")
```

### Example 2: 与学习系统集成

```python
# 自动化学习路径
class LearningPath:
    async def create_curriculum(self, library: str, topics: list):
        """创建学习课程"""

        lib = await resolve_library_id(libraryName=library)

        curriculum = {
            "library": lib['name'],
            "trust_score": lib['trust_score'],
            "lessons": []
        }

        for i, topic in enumerate(topics, 1):
            docs = await get_library_docs(
                context7CompatibleLibraryID=lib['id'],
                topic=topic,
                tokens=4000
            )

            curriculum['lessons'].append({
                "lesson_number": i,
                "topic": topic,
                "content": docs['documentation'],
                "practice": self.extract_exercises(docs['documentation'])
            })

        return curriculum

# 使用
path = LearningPath()
curriculum = await path.create_curriculum(
    library="react",
    topics=["components", "props", "state", "effects", "hooks"]
)
```

### Example 3: 与文档生成集成

```python
# 自动生成API文档
async def generate_api_docs(dependencies: dict):
    """生成项目依赖的API文档"""

    api_docs = {}

    for package, version in dependencies.items():
        # 获取包文档
        lib = await resolve_library_id(libraryName=package)
        docs = await get_library_docs(
            context7CompatibleLibraryID=f"{lib['id']}/{version}",
            tokens=5000
        )

        api_docs[package] = {
            "version": version,
            "documentation": docs['documentation'],
            "official_link": f"https://www.npmjs.com/package/{package}"
        }

    # 生成汇总文档
    generate_markdown_docs(api_docs)

# 使用
dependencies = {
    "react": "18.2.0",
    "next": "14.1.0",
    "tailwindcss": "3.4.0"
}
await generate_api_docs(dependencies)
```

## Tips & Tricks

1. **名称匹配**: 使用官方包名或产品名提高匹配准确度
2. **主题聚焦**: 明确的topic可节省50%+ tokens
3. **版本管理**: 需要特定版本时使用`/org/project/version`格式
4. **质量评估**: Trust Score ≥7 且 Code Snippets ≥100 的库更可靠
5. **Token优化**: 先用2000 tokens测试，不够再增加
6. **缓存策略**: 频繁查询的文档建议本地缓存
7. **多库对比**: 对比学习时并行查询多个库
8. **代码提取**: 使用正则提取markdown代码块
9. **更新频率**: Context7保持文档最新，无需担心过期
10. **错误处理**: resolve失败时尝试更通用的关键词

## Context7 Tools Reference

### resolve-library-id

**用途**: 将库名称解析为Context7兼容ID

**参数**:
- `libraryName` (string, required): 库名称

**返回**:
```typescript
{
  id: string,              // Context7 Library ID
  name: string,            // 库名称
  description: string,     // 库描述
  trust_score: number,     // 信任分数 0-10
  code_snippets: number    // 代码片段数量
}
```

### get-library-docs

**用途**: 获取库的文档和代码示例

**参数**:
- `context7CompatibleLibraryID` (string, required): 库ID
- `topic` (string, optional): 主题关键词
- `tokens` (number, optional): Token限制，默认5000

**返回**:
```typescript
{
  library_id: string,
  topic: string,
  documentation: string,  // Markdown格式文档
  tokens_used: number
}
```

## Version History

- **v1.0.0** (2025-10-23): 初始版本
  - resolve-library-id库名称解析
  - get-library-docs文档检索
  - 支持topic聚焦
  - Token控制
  - 版本化文档支持
