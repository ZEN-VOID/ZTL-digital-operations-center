#!/bin/bash

# ZTL餐饮数智化平面设计工作台 - 依赖检查脚本
# 检查HOOKS系统所需的所有依赖

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${CYAN}🔧 ZTL餐饮数智化平面设计工作台 - 依赖检查${NC}"
echo "📍 项目根目录: $PROJECT_ROOT"
echo

# 检查bash
echo -e "${CYAN}📋 检查bash...${NC}"
if command -v bash >/dev/null 2>&1; then
    bash_version=$(bash --version | head -n1)
    echo -e "${GREEN}✅ bash可用: $bash_version${NC}"
else
    echo -e "${RED}❌ bash不可用${NC}"
    exit 1
fi

# 检查jq
echo -e "${CYAN}📋 检查jq...${NC}"
jq_found=false

# 检查系统PATH中的jq
if command -v jq >/dev/null 2>&1; then
    jq_version=$(jq --version)
    echo -e "${GREEN}✅ 系统jq可用: $jq_version${NC}"
    jq_found=true
fi

# 检查项目根目录的jq.exe
if [[ -f "$PROJECT_ROOT/jq.exe" ]]; then
    if jq_version=$("$PROJECT_ROOT/jq.exe" --version 2>/dev/null); then
        echo -e "${GREEN}✅ 项目jq可用: $jq_version${NC}"
        jq_found=true
    else
        echo -e "${YELLOW}⚠️  项目jq文件存在但无法执行${NC}"
    fi
fi

if [[ "$jq_found" == false ]]; then
    echo -e "${RED}❌ jq不可用${NC}"
    echo -e "${YELLOW}💡 请运行以下命令安装jq:${NC}"
    echo "   Windows: powershell -ExecutionPolicy Bypass -File scripts/setup-jq.ps1"
    echo "   Linux/macOS: sudo apt-get install jq 或 brew install jq"
    exit 1
fi

# 检查HOOKS配置
echo -e "${CYAN}📋 检查HOOKS配置...${NC}"
hooks_config="$PROJECT_ROOT/.claude/settings.json"
if [[ -f "$hooks_config" ]]; then
    echo -e "${GREEN}✅ HOOKS配置文件存在${NC}"
    
    # 检查配置文件是否包含hooks配置
    if grep -q '"hooks"' "$hooks_config"; then
        echo -e "${GREEN}✅ HOOKS配置已启用${NC}"
    else
        echo -e "${YELLOW}⚠️  HOOKS配置文件存在但未配置hooks${NC}"
    fi
else
    echo -e "${RED}❌ HOOKS配置文件不存在: $hooks_config${NC}"
    exit 1
fi

# 检查HOOKS脚本
echo -e "${CYAN}📋 检查HOOKS脚本...${NC}"
hooks_dir="$PROJECT_ROOT/.claude/hooks"
if [[ -d "$hooks_dir" ]]; then
    echo -e "${GREEN}✅ HOOKS目录存在${NC}"
    
    # 检查关键脚本
    log_script="$hooks_dir/log-tool-usage.sh"
    if [[ -f "$log_script" ]]; then
        echo -e "${GREEN}✅ 日志脚本存在${NC}"
        
        # 检查脚本是否可执行
        if [[ -x "$log_script" ]]; then
            echo -e "${GREEN}✅ 日志脚本可执行${NC}"
        else
            echo -e "${YELLOW}⚠️  日志脚本不可执行，正在修复...${NC}"
            chmod +x "$log_script"
            echo -e "${GREEN}✅ 日志脚本权限已修复${NC}"
        fi
    else
        echo -e "${RED}❌ 日志脚本不存在: $log_script${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ HOOKS目录不存在: $hooks_dir${NC}"
    exit 1
fi

# 检查日志目录
echo -e "${CYAN}📋 检查日志目录...${NC}"
logs_dir="$PROJECT_ROOT/.claude/logs"
if [[ -d "$logs_dir" ]]; then
    echo -e "${GREEN}✅ 日志目录存在${NC}"
else
    echo -e "${YELLOW}⚠️  日志目录不存在，正在创建...${NC}"
    mkdir -p "$logs_dir"
    echo -e "${GREEN}✅ 日志目录已创建${NC}"
fi

# 测试HOOKS脚本
echo -e "${CYAN}📋 测试HOOKS脚本...${NC}"
test_input='{"tool_name": "dependency_check_test"}'
if echo "$test_input" | bash "$log_script" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ HOOKS脚本测试成功${NC}"
else
    echo -e "${RED}❌ HOOKS脚本测试失败${NC}"
    exit 1
fi

echo
echo -e "${GREEN}🎉 所有依赖检查通过！${NC}"
echo -e "${CYAN}📋 HOOKS系统已准备就绪${NC}"
