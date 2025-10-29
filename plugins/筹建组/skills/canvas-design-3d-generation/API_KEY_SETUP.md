# Replicate API Key 配置指南

> 本指南说明如何获取和配置TripoSR所需的Replicate API Token

---

## 📋 为什么需要API Key？

**TripoSR技能包使用Replicate平台的API**来调用TripoSR模型，原因如下：

1. **无需本地GPU**: Replicate在云端运行，无需购买昂贵的GPU硬件
2. **按需付费**: 只为实际使用付费，无月费/订阅费
3. **零维护成本**: 无需自己部署、更新模型
4. **高可用性**: 99.9%服务可用性，自动扩容

**成本参考**:
- 单个3D模型: $0.01-0.05
- 典型项目(6个场景): $0.24
- 新用户免费额度: $5-10

---

## 🔑 获取API Token

### Step 1: 注册Replicate账号

1. 访问注册页面: https://replicate.com/signup
2. 选择注册方式:
   - GitHub账号登录 (推荐)
   - Google账号登录
   - 邮箱注册

3. 完成注册流程

**注意**: 注册**完全免费**，且通常会赠送$5-10免费额度

### Step 2: 创建API Token

1. 登录后访问: https://replicate.com/account/api-tokens

2. 点击 **"Create token"** 按钮

3. 填写Token信息:
   - **Name**: 例如 "ZTL-3D-Generation" (便于识别)
   - **Permissions**: 选择 "Read and Write" (默认)

4. 点击 **"Create"** 创建Token

5. **重要**: 立即复制Token并保存
   - Token格式: `r8_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ Token只显示一次，关闭页面后无法再次查看
   - 如果忘记，只能删除旧Token并创建新Token

### Step 3: 配置API Token

选择以下任一方式配置Token：

#### 方式A: 环境变量 (推荐)

**macOS / Linux**:

```bash
# 临时设置 (仅当前终端有效)
export REPLICATE_API_TOKEN="r8_your_token_here"

# 验证设置成功
echo $REPLICATE_API_TOKEN

# 永久设置 (添加到shell配置文件)
echo 'export REPLICATE_API_TOKEN="r8_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows PowerShell**:

```powershell
# 临时设置
$env:REPLICATE_API_TOKEN="r8_your_token_here"

# 永久设置 (系统环境变量)
[System.Environment]::SetEnvironmentVariable('REPLICATE_API_TOKEN', 'r8_your_token_here', 'User')
```

#### 方式B: 代码中传入

修改 `api_client.py`:

```python
from scripts.api_client import TripoSRClient

# 直接传入Token (不推荐,仅测试使用)
client = TripoSRClient(api_token="r8_your_token_here")
```

⚠️ **不推荐**: Token会暴露在代码中，容易泄露

#### 方式C: .env文件 (推荐用于开发)

1. 创建 `.env` 文件:

```bash
cd /path/to/canvas-design-3d-generation
cat > .env << 'EOF'
REPLICATE_API_TOKEN=r8_your_token_here
EOF
```

2. 添加到 `.gitignore`:

```bash
echo ".env" >> .gitignore
```

3. 修改代码加载 `.env`:

```python
from dotenv import load_dotenv
load_dotenv()

client = TripoSRClient()  # 自动从.env读取
```

---

## ✅ 验证配置

运行测试脚本验证Token是否配置正确:

```bash
cd /Users/vincentlee/Desktop/ZTL数智化作战中心/plugins/筹建组/skills/canvas-design-3d-generation

# 测试API连接
python -c "
import os
token = os.getenv('REPLICATE_API_TOKEN')
if token:
    print(f'✅ Token已配置: {token[:10]}...')
else:
    print('❌ Token未配置,请设置REPLICATE_API_TOKEN环境变量')
"
```

**预期输出**:
```
✅ Token已配置: r8_xxxxxxxx...
```

---

## 💰 计费和成本控制

### 计费模式

**按使用量计费 (Pay-as-you-go)**:
- 无月费/订阅费
- 只为实际使用付费
- 精确到毫秒级计费

**TripoSR定价**:
- 基础成本: $0.005-0.01/秒
- 平均生成时间: 10-30秒
- 单模型成本: **$0.01-0.05**

### 成本估算

**典型项目 (300㎡火锅店)**:
```
场景数量: 6个
单模型成本: $0.04
总成本: 6 × $0.04 = $0.24

免费额度($10)可生成: 250个模型
```

**大规模批量**:
```
100个场景: 100 × $0.04 = $4.00
500个场景: 500 × $0.04 = $20.00
1000个场景: 1000 × $0.04 = $40.00
```

### 设置账单限额

为避免意外超支，建议设置账单限额:

1. 访问账单页面: https://replicate.com/account/billing
2. 设置 **Spending Limit** (例如: $50/月)
3. 配置账单提醒:
   - 50%额度消耗时提醒
   - 80%额度消耗时提醒
   - 100%额度消耗时停止服务

### 查看账单

实时查看API使用情况:

```bash
# 方式1: Web界面
https://replicate.com/account/billing

# 方式2: API查询 (需要curl)
curl -H "Authorization: Token $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/account
```

---

## 🔒 安全最佳实践

### DO ✅ 正确做法

1. **使用环境变量**: 永远不要硬编码在代码中
2. **添加到.gitignore**: 防止提交到Git
3. **定期轮换**: 每3-6个月更换Token
4. **最小权限**: 仅授予必要的API权限
5. **设置限额**: 防止意外超支
6. **监控使用**: 定期检查API调用记录

### DON'T ❌ 错误做法

1. **硬编码**: `api_token = "r8_xxxx"` 写在代码中
2. **提交到Git**: Token泄露在公开仓库
3. **分享**: 通过聊天工具发送Token
4. **公开**: 写在文档、截图、视频中
5. **共用**: 多人共用同一个Token
6. **永不更换**: 使用同一个Token超过1年

### Token泄露怎么办？

**立即行动**:

1. **撤销Token**: https://replicate.com/account/api-tokens
   - 点击泄露Token旁的 "Revoke" 按钮

2. **创建新Token**: 按照上述步骤创建新Token

3. **检查账单**: 查看是否有异常使用

4. **通知Replicate**: 如果发现恶意使用，联系support@replicate.com

5. **更新代码**: 在所有使用处更新为新Token

---

## 🏠 本地部署方案 (免API Key)

如果不想使用API，可以本地部署TripoSR开源版本:

### 系统要求

```yaml
硬件:
  - GPU: NVIDIA RTX 3060+ (8GB+ VRAM)
  - 内存: 16GB+
  - 存储: 5GB+ (模型权重)
  - 系统: Ubuntu 20.04+ / Windows 10+

软件:
  - Python: 3.9+
  - CUDA: 11.8+
  - PyTorch: 2.0+
```

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/VAST-AI-Research/TripoSR.git
cd TripoSR

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型权重 (自动,首次运行时)
python run.py --help
```

### 本地运行

```bash
# 单图生成
python run.py \
    --image input.png \
    --output output.glb \
    --device cuda

# 批量生成
python batch_run.py \
    --input_dir inputs/ \
    --output_dir outputs/ \
    --device cuda
```

### 对比表

| 维度 | Replicate API | 本地部署 |
|------|--------------|----------|
| **成本** | $0.04/模型 | 免费(电费) |
| **速度** | 10-30秒 | 20-60秒 |
| **GPU要求** | 无 | RTX 3060+ |
| **维护** | 无 | 需定期更新 |
| **推荐场景** | 中小规模,快速原型 | 大规模批量,数据敏感 |

---

## 🔧 故障排查

### 问题1: "未找到REPLICATE_API_TOKEN环境变量"

**原因**: Token未正确配置

**解决方案**:
```bash
# 检查环境变量
echo $REPLICATE_API_TOKEN

# 如果为空,重新设置
export REPLICATE_API_TOKEN="r8_your_token_here"
```

### 问题2: "401 Unauthorized"

**原因**: Token无效或已过期

**解决方案**:
1. 检查Token是否正确复制 (无多余空格/换行)
2. 访问 https://replicate.com/account/api-tokens 验证Token状态
3. 如果Token被撤销,创建新Token

### 问题3: "429 Too Many Requests"

**原因**: API调用速率超限

**解决方案**:
```python
# 在config中添加限流配置
"batch_config": {
    "max_concurrent": 1,  # 降低并发数
    "retry_delay_seconds": 10  # 增加重试延迟
}
```

### 问题4: "账单额度不足"

**原因**: 免费额度用完或设置的限额已达

**解决方案**:
1. 访问 https://replicate.com/account/billing
2. 添加支付方式 (信用卡)
3. 调整 Spending Limit

### 问题5: "生成失败,返回空结果"

**原因**: 输入图像质量问题

**解决方案**:
- 检查图像分辨率 (推荐≥512x512)
- 确保图像清晰无模糊
- 使用PNG格式 (避免JPEG压缩)

---

## 📚 相关资源

- **Replicate官网**: https://replicate.com
- **API文档**: https://replicate.com/docs
- **TripoSR模型页**: https://replicate.com/stability-ai/triposr
- **TripoSR GitHub**: https://github.com/VAST-AI-Research/TripoSR
- **定价详情**: https://replicate.com/pricing

---

## 📞 获取帮助

**Replicate支持**:
- 文档: https://replicate.com/docs
- 社区: https://discord.gg/replicate
- 邮件: support@replicate.com

**TripoSR技术问题**:
- GitHub Issues: https://github.com/VAST-AI-Research/TripoSR/issues
- 论文: https://arxiv.org/abs/2403.02151

**ZTL项目内部**:
- 查看: `reports/Phase3-3D生成技术调研报告.md`
- 测试: `plugins/筹建组/skills/canvas-design-3d-generation/test_integration.py`

---

**文档版本**: v1.0.0
**更新日期**: 2025-10-28
**维护者**: Z3-3D生成AIGC助手
