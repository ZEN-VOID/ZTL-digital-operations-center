---
description: 彻底清理 /trees 命令产生的所有工作树、分支和目录残留
---

# Trees 清理命令

请彻底清理 `/trees` 命令产生的所有残留内容,按以下步骤执行:

## 执行步骤

### 1. 获取工作树列表

```bash
# 获取所有工作树路径(排除主工作目录)
git worktree list --porcelain | grep "^worktree" | awk '{print $2}' | grep "trees/"
```

### 2. 移除所有工作树

对于每个工作树路径:
```bash
# 强制移除工作树(包含未提交更改)
git worktree remove --force <path>
```

如果有多个工作树,批量处理:
```bash
git worktree list --porcelain | grep "^worktree" | awk '{print $2}' | grep "trees/" | while read path; do
  echo "Removing worktree: $path"
  git worktree remove --force "$path" 2>/dev/null || true
done
```

### 3. 删除对应分支

```bash
# 获取所有分支(排除当前分支、main、main-clean、master)
git branch | grep -v "^\*" | grep -v -E "^\s*(main|main-clean|master)$" | xargs -I {} git branch -D {}
```

### 4. 清理 trees/ 目录

```bash
# 删除 trees/ 下除了 README.md 之外的所有内容
find trees -mindepth 1 -maxdepth 1 ! -name 'README.md' -exec rm -rf {} +
```

### 5. 清理 Git 工作树引用

```bash
git worktree prune -v
```

### 6. 最终验证

```bash
echo "=== 当前工作树 ==="
git worktree list

echo ""
echo "=== 当前分支 ==="
git branch

echo ""
echo "=== trees/ 目录内容 ==="
ls -la trees/
```

## 一键执行脚本

你可以直接执行以下完整脚本:

```bash
#!/bin/bash

echo "🧹 开始清理 Trees 工作树..."
echo ""

# 统计变量
removed_worktrees=0
deleted_branches=0
deleted_files=0

# 1. 移除所有工作树
echo "📋 步骤 1/5: 移除工作树"
git worktree list --porcelain | grep "^worktree" | awk '{print $2}' | grep "trees/" | while read path; do
  if [ -n "$path" ]; then
    echo "  - 移除: $path"
    git worktree remove --force "$path" 2>/dev/null && ((removed_worktrees++))
  fi
done

# 2. 删除分支
echo ""
echo "📋 步骤 2/5: 删除分支"
branches_to_delete=$(git branch | grep -v "^\*" | grep -v -E "^\s*(main|main-clean|master)$" | tr -d ' ')
if [ -n "$branches_to_delete" ]; then
  echo "$branches_to_delete" | while read branch; do
    if [ -n "$branch" ]; then
      echo "  - 删除分支: $branch"
      git branch -D "$branch" 2>/dev/null && ((deleted_branches++))
    fi
  done
else
  echo "  ✅ 没有需要删除的分支"
fi

# 3. 清理 trees/ 目录
echo ""
echo "📋 步骤 3/5: 清理 trees/ 目录"
deleted_files=$(find trees -mindepth 1 -maxdepth 1 ! -name 'README.md' | wc -l | tr -d ' ')
if [ "$deleted_files" -gt 0 ]; then
  find trees -mindepth 1 -maxdepth 1 ! -name 'README.md' -exec rm -rf {} +
  echo "  ✅ 删除了 $deleted_files 个文件/目录"
else
  echo "  ✅ trees/ 目录已经干净"
fi

# 4. 清理 Git 引用
echo ""
echo "📋 步骤 4/5: 清理 Git 工作树引用"
git worktree prune -v
echo "  ✅ 引用已清理"

# 5. 最终验证
echo ""
echo "📋 步骤 5/5: 最终验证"
echo ""
echo "=== 当前工作树 ==="
git worktree list
echo ""
echo "=== 当前分支 ==="
git branch
echo ""
echo "=== trees/ 目录内容 ==="
ls -la trees/

echo ""
echo "✅ Trees 清理完成!"
echo ""
echo "清理报告:"
echo "  - 移除工作树: 已完成"
echo "  - 删除分支: 已完成"
echo "  - 清理目录: $deleted_files 个文件/目录"
echo "  - Git 引用: 已清理"
echo ""
echo "当前状态:"
echo "  - 工作树: 仅主目录 ($(git branch --show-current))"
echo "  - trees/ 目录: 仅保留 README.md ✅"
```

## 使用说明

执行此命令后,我会:

1. ✅ 移除所有 trees/ 目录下的工作树
2. ✅ 删除所有相关分支(保护 main/main-clean/master)
3. ✅ 清理 trees/ 目录下的所有文件和子目录(保留 README.md)
4. ✅ 清理 Git 工作树的内部引用
5. ✅ 提供详细的清理报告

## 安全保护

- ❌ 不删除当前分支
- ❌ 不删除 main/main-clean/master 分支
- ✅ 强制保留 trees/README.md
- ✅ 使用 --force 自动处理未提交的更改
- ✅ 所有操作带错误处理,不会中断清理流程
