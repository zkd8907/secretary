# Secretary - 特朗普社交媒体分析助手

## 项目简介

Secretary 是一个自动化的社交媒体分析工具，专门用于监控和分析特朗普在 Truth Social 平台上的发言，并通过 AI 进行内容分析和市场影响评估。该工具能够自动抓取特朗普的最新发言，进行翻译和分析，并将分析结果通过企业微信机器人推送给指定用户。

## 主要功能

- 自动抓取特朗普在 Truth Social 上的最新发言
- 使用 AI 进行内容翻译和分析
- 评估发言对多个市场的影响，包括：
  - 美股市场
  - 美债市场
  - 科技股
  - 半导体股
  - 中国股票市场
  - 香港股票市场
  - 美元汇率
  - 中美关系
- 通过企业微信机器人推送分析结果

## 技术栈

- Python 3.11+
- LangChain
- Truthbrush
- 企业微信机器人 API

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/secretary.git
cd secretary
```

2. 创建并激活虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -e .
```

4. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```
# Redis 配置
REDIS_URL=redis://your_redis_url

# Truth Social 配置
TRUTHSOCIAL_TOKEN=your_truthsocial_token

# 腾讯混元大模型配置
HUNYUAN_API_KEY=your_hunyuan_api_key
HUNYUAN_API_BASE=https://api.hunyuan.cloud.tencent.com/v1

# 企业微信机器人配置
WECOM_ROBOT_ID=your_wecom_robot_id
```

环境变量说明：
- `REDIS_URL`: Redis 数据库连接地址，用于数据缓存
- `TRUTHSOCIAL_TOKEN`: Truth Social 平台的访问令牌
- `HUNYUAN_API_KEY`: 腾讯混元大模型的 API 密钥
- `HUNYUAN_API_BASE`: 腾讯混元大模型的 API 基础地址
- `WECOM_ROBOT_ID`: 企业微信机器人的 ID

## 使用方法

1. 确保已正确配置环境变量
2. 运行主程序：
```bash
python main.py
```

程序会自动：
- 抓取特朗普的最新发言
- 进行 AI 分析和翻译
- 评估市场影响
- 通过企业微信机器人推送分析结果

## 输出格式

分析结果将以 Markdown 格式推送，包含：
- 发言时间
- 原文内容
- 中文翻译
- 市场影响分析（仅显示非中性的影响）

## 注意事项

- 确保网络连接正常
- 企业微信机器人需要正确配置
- 建议使用 Python 3.11 或更高版本
- 需要有效的企业微信机器人 ID

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
