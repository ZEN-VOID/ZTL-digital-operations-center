---
name: GitHub Code Collaboration
description: GitHub代码协作全流程管理，涵盖仓库管理、文件操作、分支提交、Issue跟踪、Pull Request审查等25+核心功能，支持团队协作和代码版本控制
---

# GitHub MCP Skill

基于github-mcp的GitHub代码协作能力包，提供从仓库创建到代码合并的完整开发流程支持。

## Quick Start

### 示例1: 创建仓库并推送代码

```python
# 1. 创建仓库
await mcp__github_mcp__create_repository(
    name="my-awesome-project",
    description="A demo project",
    private=False,
    autoInit=True
)

# 2. 创建或更新文件
await mcp__github_mcp__create_or_update_file(
    owner="username",
    repo="my-awesome-project",
    path="README.md",
    content="# My Awesome Project\n\nWelcome!",
    message="Initial commit",
    branch="main"
)

# 3. 批量推送多个文件
await mcp__github_mcp__push_files(
    owner="username",
    repo="my-awesome-project",
    branch="main",
    files=[
        {"path": "src/main.py", "content": "print('Hello')"},
        {"path": "requirements.txt", "content": "requests==2.31.0"}
    ],
    message="Add source files"
)
```

### 示例2: 创建Issue并跟踪

```python
# 1. 创建Issue
issue = await mcp__github_mcp__create_issue(
    owner="username",
    repo="project",
    title="Bug: Login fails with special characters",
    body="## Description\nUsers cannot login when password contains @ symbol",
    labels=["bug", "high-priority"],
    assignees=["developer1"]
)

# 2. 添加评论
await mcp__github_mcp__add_issue_comment(
    owner="username",
    repo="project",
    issue_number=issue['number'],
    body="Investigating this issue. Will update soon."
)

# 3. 更新Issue状态
await mcp__github_mcp__update_issue(
    owner="username",
    repo="project",
    issue_number=issue['number'],
    state="closed",
    body="Fixed in PR #123"
)
```

### 示例3: Pull Request工作流

```python
# 1. 创建新分支
await mcp__github_mcp__create_branch(
    owner="username",
    repo="project",
    branch="feature/user-authentication",
    from_branch="main"
)

# 2. 推送代码到新分支
await mcp__github_mcp__push_files(
    owner="username",
    repo="project",
    branch="feature/user-authentication",
    files=[{"path": "auth.py", "content": "..."}],
    message="Implement user authentication"
)

# 3. 创建Pull Request
pr = await mcp__github_mcp__create_pull_request(
    owner="username",
    repo="project",
    title="feat: Add user authentication",
    head="feature/user-authentication",
    base="main",
    body="## Changes\n- Add login/logout\n- Add session management",
    draft=False
)

# 4. 审查Pull Request
await mcp__github_mcp__create_pull_request_review(
    owner="username",
    repo="project",
    pull_number=pr['number'],
    body="LGTM! Great implementation.",
    event="APPROVE",
    comments=[
        {
            "path": "auth.py",
            "line": 42,
            "body": "Consider adding error handling here"
        }
    ]
)

# 5. 合并Pull Request
await mcp__github_mcp__merge_pull_request(
    owner="username",
    repo="project",
    pull_number=pr['number'],
    merge_method="squash",
    commit_title="feat: Add user authentication",
    commit_message="Implements login/logout and session management"
)
```

## Core Capabilities

### 1. 仓库管理 (Repository Management)

#### 1.1 创建仓库
```python
await mcp__github_mcp__create_repository(
    name="repo-name",
    description="Repository description",
    private=False,  # 公开仓库
    autoInit=True   # 自动初始化README
)
```

#### 1.2 搜索仓库
```python
repos = await mcp__github_mcp__search_repositories(
    query="language:python stars:>1000 topic:machine-learning",
    page=1,
    perPage=10
)
```

#### 1.3 Fork仓库
```python
await mcp__github_mcp__fork_repository(
    owner="original-owner",
    repo="original-repo",
    organization="my-org"  # 可选，fork到指定组织
)
```

### 2. 文件操作 (File Operations)

#### 2.1 获取文件内容
```python
file_data = await mcp__github_mcp__get_file_contents(
    owner="username",
    repo="project",
    path="src/config.json",
    branch="main"  # 可选
)
```

#### 2.2 创建或更新单个文件
```python
await mcp__github_mcp__create_or_update_file(
    owner="username",
    repo="project",
    path="docs/api.md",
    content="# API Documentation\n...",
    message="Update API docs",
    branch="main",
    sha="abc123..."  # 更新现有文件时需要提供
)
```

#### 2.3 批量推送文件
```python
await mcp__github_mcp__push_files(
    owner="username",
    repo="project",
    branch="develop",
    files=[
        {"path": "file1.py", "content": "content1"},
        {"path": "file2.py", "content": "content2"}
    ],
    message="Batch update"
)
```

### 3. 分支与提交管理 (Branch & Commit Management)

#### 3.1 创建分支
```python
await mcp__github_mcp__create_branch(
    owner="username",
    repo="project",
    branch="feature/new-feature",
    from_branch="develop"  # 可选，默认从默认分支创建
)
```

#### 3.2 查看提交历史
```python
commits = await mcp__github_mcp__list_commits(
    owner="username",
    repo="project",
    sha="main",  # 可选，指定分支或commit
    page=1,
    perPage=20
)
```

### 4. Issue管理 (Issue Management)

#### 4.1 创建Issue
```python
await mcp__github_mcp__create_issue(
    owner="username",
    repo="project",
    title="Issue title",
    body="Detailed description",
    labels=["bug", "priority-high"],
    assignees=["user1", "user2"],
    milestone=1  # 可选，里程碑编号
)
```

#### 4.2 列出Issues
```python
issues = await mcp__github_mcp__list_issues(
    owner="username",
    repo="project",
    state="open",  # open/closed/all
    labels=["bug"],
    sort="created",  # created/updated/comments
    direction="desc",  # asc/desc
    page=1,
    per_page=30
)
```

#### 4.3 更新Issue
```python
await mcp__github_mcp__update_issue(
    owner="username",
    repo="project",
    issue_number=42,
    title="Updated title",
    body="Updated description",
    state="closed",
    labels=["resolved"],
    assignees=["maintainer"]
)
```

#### 4.4 添加评论
```python
await mcp__github_mcp__add_issue_comment(
    owner="username",
    repo="project",
    issue_number=42,
    body="This is fixed in version 2.0"
)
```

#### 4.5 获取Issue详情
```python
issue = await mcp__github_mcp__get_issue(
    owner="username",
    repo="project",
    issue_number=42
)
```

### 5. Pull Request管理 (Pull Request Management)

#### 5.1 创建Pull Request
```python
pr = await mcp__github_mcp__create_pull_request(
    owner="username",
    repo="project",
    title="feat: Add new feature",
    head="feature/branch",  # 源分支
    base="main",  # 目标分支
    body="## Description\n...",
    draft=False,  # 是否创建为草稿
    maintainer_can_modify=True
)
```

#### 5.2 列出Pull Requests
```python
prs = await mcp__github_mcp__list_pull_requests(
    owner="username",
    repo="project",
    state="open",  # open/closed/all
    head="username:feature-branch",  # 可选，过滤源分支
    base="main",  # 可选，过滤目标分支
    sort="created",  # created/updated/popularity/long-running
    direction="desc",
    page=1,
    per_page=30
)
```

#### 5.3 获取PR详情
```python
pr = await mcp__github_mcp__get_pull_request(
    owner="username",
    repo="project",
    pull_number=123
)
```

#### 5.4 获取PR变更文件
```python
files = await mcp__github_mcp__get_pull_request_files(
    owner="username",
    repo="project",
    pull_number=123
)
```

#### 5.5 获取PR状态检查
```python
status = await mcp__github_mcp__get_pull_request_status(
    owner="username",
    repo="project",
    pull_number=123
)
```

#### 5.6 创建PR审查
```python
await mcp__github_mcp__create_pull_request_review(
    owner="username",
    repo="project",
    pull_number=123,
    body="Review summary",
    event="APPROVE",  # APPROVE/REQUEST_CHANGES/COMMENT
    commit_id="abc123...",  # 可选
    comments=[
        {
            "path": "src/main.py",
            "position": 10,  # 或使用 line: 20
            "body": "Suggestion: use constant here"
        }
    ]
)
```

#### 5.7 合并Pull Request
```python
await mcp__github_mcp__merge_pull_request(
    owner="username",
    repo="project",
    pull_number=123,
    merge_method="squash",  # merge/squash/rebase
    commit_title="feat: Feature title",
    commit_message="Detailed description"
)
```

#### 5.8 更新PR分支
```python
await mcp__github_mcp__update_pull_request_branch(
    owner="username",
    repo="project",
    pull_number=123,
    expected_head_sha="abc123..."  # 可选，安全检查
)
```

#### 5.9 获取PR评论
```python
comments = await mcp__github_mcp__get_pull_request_comments(
    owner="username",
    repo="project",
    pull_number=123
)
```

#### 5.10 获取PR审查记录
```python
reviews = await mcp__github_mcp__get_pull_request_reviews(
    owner="username",
    repo="project",
    pull_number=123
)
```

### 6. 搜索功能 (Search)

#### 6.1 搜索代码
```python
results = await mcp__github_mcp__search_code(
    q="function:authenticate language:python repo:username/project",
    sort="indexed",  # 可选
    order="desc",  # asc/desc
    page=1,
    per_page=30
)
```

#### 6.2 搜索Issues和PRs
```python
results = await mcp__github_mcp__search_issues(
    q="is:open is:issue label:bug repo:username/project",
    sort="created",  # comments/created/updated
    order="desc",
    page=1,
    per_page=30
)
```

#### 6.3 搜索用户
```python
users = await mcp__github_mcp__search_users(
    q="location:Beijing language:Python",
    sort="followers",  # followers/repositories/joined
    order="desc",
    page=1,
    per_page=30
)
```

## Usage Patterns

### Pattern 1: 功能分支开发流程

```python
async def feature_branch_workflow(owner, repo, feature_name, files):
    """完整的功能分支开发流程"""

    # 1. 创建功能分支
    branch_name = f"feature/{feature_name}"
    await mcp__github_mcp__create_branch(
        owner=owner,
        repo=repo,
        branch=branch_name,
        from_branch="develop"
    )

    # 2. 推送代码变更
    await mcp__github_mcp__push_files(
        owner=owner,
        repo=repo,
        branch=branch_name,
        files=files,
        message=f"feat: Implement {feature_name}"
    )

    # 3. 创建Pull Request
    pr = await mcp__github_mcp__create_pull_request(
        owner=owner,
        repo=repo,
        title=f"feat: {feature_name}",
        head=branch_name,
        base="develop",
        body=f"## Feature: {feature_name}\n\nImplementation details..."
    )

    # 4. 等待审查和测试...

    # 5. 合并PR
    await mcp__github_mcp__merge_pull_request(
        owner=owner,
        repo=repo,
        pull_number=pr['number'],
        merge_method="squash"
    )

    return pr
```

### Pattern 2: Issue驱动开发

```python
async def issue_driven_development(owner, repo, issue_number):
    """基于Issue的开发流程"""

    # 1. 获取Issue详情
    issue = await mcp__github_mcp__get_issue(
        owner=owner,
        repo=repo,
        issue_number=issue_number
    )

    # 2. 创建修复分支
    branch_name = f"fix/issue-{issue_number}"
    await mcp__github_mcp__create_branch(
        owner=owner,
        repo=repo,
        branch=branch_name
    )

    # 3. 实现修复并推送
    # ... 代码实现 ...

    # 4. 创建PR并关联Issue
    pr = await mcp__github_mcp__create_pull_request(
        owner=owner,
        repo=repo,
        title=f"fix: {issue['title']}",
        head=branch_name,
        base="main",
        body=f"Fixes #{issue_number}\n\n{issue['body']}"
    )

    # 5. PR合并后Issue自动关闭
    return pr
```

### Pattern 3: 代码审查自动化

```python
async def automated_code_review(owner, repo, pull_number):
    """自动化代码审查流程"""

    # 1. 获取PR变更文件
    files = await mcp__github_mcp__get_pull_request_files(
        owner=owner,
        repo=repo,
        pull_number=pull_number
    )

    # 2. 分析代码质量
    review_comments = []
    for file in files:
        # 分析文件内容...
        if needs_review:
            review_comments.append({
                "path": file['filename'],
                "line": line_number,
                "body": "建议: ..."
            })

    # 3. 提交审查意见
    if review_comments:
        await mcp__github_mcp__create_pull_request_review(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            body="自动代码审查完成",
            event="COMMENT",
            comments=review_comments
        )
    else:
        await mcp__github_mcp__create_pull_request_review(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            body="代码质量良好，建议批准",
            event="APPROVE"
        )
```

### Pattern 4: 项目初始化

```python
async def initialize_project(name, description, template_files):
    """快速初始化新项目"""

    # 1. 创建仓库
    await mcp__github_mcp__create_repository(
        name=name,
        description=description,
        private=False,
        autoInit=True
    )

    # 2. 设置项目结构
    await mcp__github_mcp__push_files(
        owner="username",
        repo=name,
        branch="main",
        files=template_files,
        message="Initial project structure"
    )

    # 3. 创建开发分支
    await mcp__github_mcp__create_branch(
        owner="username",
        repo=name,
        branch="develop",
        from_branch="main"
    )

    # 4. 创建初始Issues
    for issue_data in get_initial_issues():
        await mcp__github_mcp__create_issue(
            owner="username",
            repo=name,
            title=issue_data['title'],
            body=issue_data['body'],
            labels=issue_data['labels']
        )
```

## Best Practices

### 1. 认证配置
- 使用GitHub Personal Access Token进行认证
- Token权限: repo, workflow, read:org (根据需求)
- 环境变量方式: `GITHUB_TOKEN=your_token_here`

### 2. 分支策略
- **main/master**: 生产分支，保护分支，仅通过PR合并
- **develop**: 开发分支，日常开发基线
- **feature/***: 功能分支，从develop创建
- **hotfix/***: 紧急修复分支，从main创建

### 3. Commit规范
使用约定式提交(Conventional Commits):
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建工具或辅助工具的变动
```

### 4. PR最佳实践
- 标题使用约定式提交格式
- Body包含详细的变更说明
- 关联相关Issue: `Fixes #123`, `Closes #456`
- 小而专注的PR，便于审查
- 及时响应审查意见

### 5. Issue管理
- 使用标签分类: bug, enhancement, documentation, question
- 设置优先级标签: priority-high, priority-medium, priority-low
- 使用模板标准化Issue格式
- 及时更新状态和进展

### 6. 错误处理
```python
try:
    pr = await mcp__github_mcp__create_pull_request(...)
except Exception as e:
    if "already exists" in str(e):
        # PR已存在，获取现有PR
        prs = await mcp__github_mcp__list_pull_requests(
            owner=owner,
            repo=repo,
            head=f"{owner}:{branch_name}",
            state="open"
        )
        pr = prs[0] if prs else None
    else:
        raise
```

## Common Issues

### Issue 1: 文件SHA不匹配
**问题**: 更新文件时提示SHA不匹配
**解决**:
```python
# 先获取最新文件内容和SHA
file_data = await mcp__github_mcp__get_file_contents(
    owner=owner,
    repo=repo,
    path=file_path
)

# 使用最新SHA更新
await mcp__github_mcp__create_or_update_file(
    owner=owner,
    repo=repo,
    path=file_path,
    content=new_content,
    message="Update file",
    sha=file_data['sha']  # 使用最新SHA
)
```

### Issue 2: PR合并冲突
**问题**: Pull Request存在合并冲突
**解决**:
```python
# 1. 更新PR分支为最新
await mcp__github_mcp__update_pull_request_branch(
    owner=owner,
    repo=repo,
    pull_number=pr_number
)

# 2. 手动解决冲突后重新推送
# 3. 或使用rebase策略
```

### Issue 3: 权限不足
**问题**: 403 Forbidden错误
**解决**:
- 检查GitHub Token权限范围
- 确认仓库访问权限
- 对于组织仓库，确认Token已授权访问组织

### Issue 4: 搜索结果不完整
**问题**: 搜索API返回结果有限
**解决**:
```python
# 使用分页获取完整结果
all_results = []
page = 1
while True:
    results = await mcp__github_mcp__search_repositories(
        query=search_query,
        page=page,
        perPage=100  # 最大值
    )
    if not results or len(results) == 0:
        break
    all_results.extend(results)
    page += 1
```

## Integration Examples

### 示例1: CI/CD集成

```python
async def ci_cd_integration(owner, repo, pr_number):
    """CI/CD流程集成"""

    # 1. 获取PR状态
    status = await mcp__github_mcp__get_pull_request_status(
        owner=owner,
        repo=repo,
        pull_number=pr_number
    )

    # 2. 检查所有检查是否通过
    all_checks_passed = all(
        check['state'] == 'success'
        for check in status.get('statuses', [])
    )

    # 3. 如果检查通过，自动合并
    if all_checks_passed:
        pr = await mcp__github_mcp__get_pull_request(
            owner=owner,
            repo=repo,
            pull_number=pr_number
        )

        # 确认有审批
        reviews = await mcp__github_mcp__get_pull_request_reviews(
            owner=owner,
            repo=repo,
            pull_number=pr_number
        )

        approved = any(r['state'] == 'APPROVED' for r in reviews)

        if approved:
            await mcp__github_mcp__merge_pull_request(
                owner=owner,
                repo=repo,
                pull_number=pr_number,
                merge_method="squash"
            )
            return True

    return False
```

### 示例2: 自动化发布流程

```python
async def automated_release(owner, repo, version, changelog):
    """自动化版本发布"""

    # 1. 创建发布分支
    release_branch = f"release/v{version}"
    await mcp__github_mcp__create_branch(
        owner=owner,
        repo=repo,
        branch=release_branch,
        from_branch="develop"
    )

    # 2. 更新版本文件
    version_files = [
        {
            "path": "VERSION",
            "content": version
        },
        {
            "path": "CHANGELOG.md",
            "content": changelog
        }
    ]

    await mcp__github_mcp__push_files(
        owner=owner,
        repo=repo,
        branch=release_branch,
        files=version_files,
        message=f"chore: Prepare release v{version}"
    )

    # 3. 创建PR到main
    pr = await mcp__github_mcp__create_pull_request(
        owner=owner,
        repo=repo,
        title=f"Release v{version}",
        head=release_branch,
        base="main",
        body=f"# Release v{version}\n\n{changelog}"
    )

    return pr
```

### 示例3: 代码迁移工具

```python
async def migrate_repository(source_owner, source_repo,
                             target_owner, target_repo):
    """仓库迁移工具"""

    # 1. Fork源仓库
    await mcp__github_mcp__fork_repository(
        owner=source_owner,
        repo=source_repo,
        organization=target_owner
    )

    # 2. 获取所有Issues并迁移
    issues = await mcp__github_mcp__list_issues(
        owner=source_owner,
        repo=source_repo,
        state="all",
        per_page=100
    )

    for issue in issues:
        await mcp__github_mcp__create_issue(
            owner=target_owner,
            repo=target_repo,
            title=issue['title'],
            body=f"Migrated from {source_owner}/{source_repo}#{issue['number']}\n\n{issue['body']}",
            labels=issue.get('labels', [])
        )

    # 3. 迁移Pull Requests (创建为Issues with PR标签)
    # ...
```

## Tips & Tricks

### 1. 批量操作优化
```python
# ❌ 避免: 循环中单个API调用
for file in files:
    await mcp__github_mcp__create_or_update_file(...)

# ✅ 推荐: 使用批量推送
await mcp__github_mcp__push_files(
    owner=owner,
    repo=repo,
    branch=branch,
    files=files,
    message="Batch update"
)
```

### 2. 搜索查询优化
```python
# 高级搜索语法
queries = [
    "repo:owner/repo language:python",  # 指定仓库和语言
    "is:open is:issue label:bug",  # Issue过滤
    "is:pr is:merged author:username",  # PR过滤
    "stars:>1000 forks:>100",  # 热门仓库
    "created:>2024-01-01",  # 时间范围
    "path:src/ extension:py"  # 文件路径过滤
]
```

### 3. PR审查技巧
```python
# 使用position参数针对diff中的特定行评论
await mcp__github_mcp__create_pull_request_review(
    owner=owner,
    repo=repo,
    pull_number=pr_number,
    comments=[
        {
            "path": "src/main.py",
            "position": 5,  # diff中的位置(从1开始)
            "body": "建议添加类型注解"
        }
    ]
)

# 或使用line参数针对文件中的绝对行号
comments=[
    {
        "path": "src/main.py",
        "line": 42,  # 文件中的行号
        "body": "建议使用常量"
    }
]
```

### 4. Draft PR工作流
```python
# 1. 创建草稿PR用于早期反馈
pr = await mcp__github_mcp__create_pull_request(
    owner=owner,
    repo=repo,
    title="WIP: Feature implementation",
    head="feature-branch",
    base="main",
    draft=True  # 创建为草稿
)

# 2. 开发完成后标记为ready
# (需要使用GitHub REST API直接调用)
```

### 5. 智能合并策略选择
```python
def choose_merge_method(pr):
    """根据PR特征选择合并方式"""
    commits_count = pr.get('commits', 0)

    if commits_count == 1:
        return "rebase"  # 单个commit，保持线性历史
    elif commits_count > 10:
        return "squash"  # 多个commit，合并为一个
    else:
        return "merge"  # 保留完整提交历史
```

### 6. Issue模板应用
```python
# 在Issue body中使用模板
issue_template = """
## Bug描述
{description}

## 复现步骤
1. {step1}
2. {step2}

## 期望行为
{expected}

## 实际行为
{actual}

## 环境信息
- OS: {os}
- Version: {version}
"""

await mcp__github_mcp__create_issue(
    owner=owner,
    repo=repo,
    title=title,
    body=issue_template.format(**issue_data),
    labels=["bug"]
)
```

### 7. 分支保护规则检查
```python
async def check_branch_protection(owner, repo, pr_number):
    """检查PR是否满足分支保护要求"""

    # 1. 获取PR状态
    status = await mcp__github_mcp__get_pull_request_status(
        owner=owner,
        repo=repo,
        pull_number=pr_number
    )

    # 2. 检查必需的状态检查
    required_checks = ['ci/test', 'ci/lint', 'ci/build']
    passed_checks = [
        check['context']
        for check in status.get('statuses', [])
        if check['state'] == 'success'
    ]

    all_required_passed = all(
        check in passed_checks
        for check in required_checks
    )

    # 3. 检查审查要求
    reviews = await mcp__github_mcp__get_pull_request_reviews(
        owner=owner,
        repo=repo,
        pull_number=pr_number
    )

    approvals = sum(1 for r in reviews if r['state'] == 'APPROVED')

    return all_required_passed and approvals >= 2
```

### 8. 自动化标签管理
```python
async def auto_label_pr(owner, repo, pr_number):
    """根据PR内容自动添加标签"""

    # 获取PR文件变更
    files = await mcp__github_mcp__get_pull_request_files(
        owner=owner,
        repo=repo,
        pull_number=pr_number
    )

    labels = []

    # 根据文件路径判断
    for file in files:
        if 'test' in file['filename']:
            labels.append('testing')
        if 'docs/' in file['filename']:
            labels.append('documentation')
        if '.py' in file['filename']:
            labels.append('python')

    # 根据变更量判断
    total_changes = sum(
        file.get('additions', 0) + file.get('deletions', 0)
        for file in files
    )

    if total_changes > 500:
        labels.append('large-changes')

    # 更新PR标签
    pr = await mcp__github_mcp__get_pull_request(
        owner=owner,
        repo=repo,
        pull_number=pr_number
    )

    # 注意: 需要转换为Issue API更新标签
    # (PR实际上是特殊的Issue)
    await mcp__github_mcp__update_issue(
        owner=owner,
        repo=repo,
        issue_number=pr_number,
        labels=list(set(labels))
    )
```
