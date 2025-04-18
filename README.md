# Secretary - 社交媒体内容分析助手

## 项目简介

Secretary 是一个自动化的社交媒体分析工具，专门用于监控和分析社交媒体平台上的内容，并通过 AI 进行智能分析。该工具能够自动抓取指定账号的最新发言，根据配置的分析提示词进行内容分析，并将分析结果通过企业微信机器人推送给指定用户。通过灵活配置分析提示词，可以针对不同主题（如财经、政治、科技等）进行定制化分析。

## 主要功能

- 支持多个社交媒体平台的监控（目前支持 Truth Social 和 Twitter）
- 可配置多个监控账号，每个账号可以设置不同的分析提示词
- 支持自定义分析主题和维度，通过配置提示词实现灵活的分析策略
- 使用 AI 进行内容翻译和分析
- 支持多维度分析，例如：
  - 财经分析（市场影响、投资机会等）
  - 政治分析（政策影响、国际关系等）
  - 科技分析（技术趋势、创新影响等）
  - 其他自定义分析维度
- 支持多个企业微信机器人，可以为不同账号配置不同的推送目标
- 支持调试模式，方便开发和测试

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/secretary.git
cd secretary
```

2. 安装并配置 uv（推荐）：
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使用 uv 安装依赖
uv sync
```

或者使用传统的 venv 方式（不推荐）：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
pip install -e .
```

3. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```
# Redis 配置
REDIS_URL=redis://your_redis_url

# Truth Social 配置
TRUTHSOCIAL_TOKEN=your_truthsocial_token

# Twitter 配置
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password

# 腾讯混元大模型配置
HUNYUAN_API_KEY=your_hunyuan_api_key
HUNYUAN_API_BASE=https://api.hunyuan.cloud.tencent.com/v1

# 企业微信机器人配置（可配置多个）
WECOM_TRUMP_ROBOT_ID=your_wecom_robot_id_1
WECOM_FINANCE_ROBOT_ID=your_wecom_robot_id_2

# 调试模式（可选）
DEBUG=1
```

4. 配置监控账号：
创建 `config/social-networks.yml` 文件，配置需要监控的社交媒体账号：
```yaml
social_networks:
  - type: truthsocial
    socialNetworkId: realDonaldTrump
    prompt: >-
      你现在是一名财经专家，请对以下美国总统的发言进行分析，并给按我指定的格式返回分析结果。
      输出格式为原始合法的json字符串，字符串中如果有一些特殊的字符需要做好转义，确保最终这个json字符串可以在python中被正确解析。
      在最终输出的内容中除了json字符串本身，不需要其它额外的信息，也不要在json内容前后额外增加markdown的三个点转义。

      这是你需要分析的内容：{content}

      这是输出格式的说明：
      {
          "is_relevant": "是否与财经相关，只需要返回1或0这两个值之一即可",
          "analytical_briefing": "分析简报"
      }

      其中analytical_briefing的值是一个字符串，它是针对内容所做的分析简报，仅在is_relevant为1时会返回这个值。

      analytical_briefing的内容是markdown格式的，它需要符合下面的规范

      ```markdown
      > 原始正文，仅当需要分析的内容为英文时，这部分内容才会以markdown中引用的格式返回，否则这部分的内容为原始的正文

      翻译后的内容，仅当需要分析的内容为英文时，才会有这部分的内容。

      ## Brief Analysis

      分析结果。这部分首页会展示一个列表，列表中分别包含美股市场、美债市场、科技股、半导体股、中国股票市场、香港股票市场、人民币兑美元汇率、中美关系这8个选项。
      每个选项的值为分别为📈利多和📉利空。如果分析内容对于该选项没有影响，就不要针对这个选项返回任何内容。

      ## Summarize

      这部分需要用非常简明扼要的文字对分析结果进行总结，以及解释为什么在上面针对不同选项会得出不同的结论。
      ```
    weComRobotEnvName: WECOM_TRUMP_ROBOT_ID
  - type: twitter
    socialNetworkId: myfxtrader
    prompt: >-
      你现在是一名财经专家，请对以下财经博主的发言进行分析，并给按我指定的格式返回分析结果。
      # ... 其他配置与上面类似 ...
    weComRobotEnvName: WECOM_FINANCE_ROBOT_ID
```

> ⚠️ **重要提示**：在配置 prompt 时，必须确保大模型返回的结果是一个合法的 JSON 字符串，并且包含以下两个必需属性：
> 1. `is_relevant`：表示内容是否相关，值为 1 或 0
> 2. `analytical_briefing`：分析简报内容，仅在 `is_relevant` 为 1 时返回
>
> 如果返回的 JSON 格式不正确或缺少必需属性，程序将无法正常处理分析结果。

环境变量说明：
- `REDIS_URL`: Redis 数据库连接地址，用于数据缓存
- `TRUTHSOCIAL_TOKEN`: Truth Social 平台的访问令牌
- `TWITTER_USERNAME`: Twitter 平台的用户名
- `TWITTER_PASSWORD`: Twitter 平台的密码
- `HUNYUAN_API_KEY`: 腾讯混元大模型的 API 密钥
- `HUNYUAN_API_BASE`: 腾讯混元大模型的 API 基础地址
- `WECOM_*_ROBOT_ID`: 企业微信机器人的 ID，可以配置多个
- `DEBUG`: 调试模式开关，设置为 1 时启用调试模式

## 使用方法

1. 确保已正确配置环境变量和监控账号
2. 运行主程序：
```bash
python main.py
```

程序会自动：
- 抓取配置的社交媒体账号的最新发言
- 根据每个账号配置的提示词进行 AI 分析和翻译
- 生成分析报告
- 通过配置的企业微信机器人推送分析结果

## 输出格式

分析结果将以 Markdown 格式推送，包含：
- 发言时间
- 原文内容（如果是英文内容会以引用格式显示）
- 中文翻译（仅当原文为英文时显示）
- 分析结果（根据提示词配置的格式）
- 分析总结

## 注意事项

- 确保网络连接正常
- 企业微信机器人需要正确配置
- 建议使用 Python 3.11 或更高版本
- 需要有效的企业微信机器人 ID
- 调试模式下，消息将直接打印到控制台而不会发送到企业微信
- 每个监控账号可以配置不同的分析提示词和推送目标
- 提示词配置决定了分析的主题和维度，可以根据需求灵活调整
- Twitter登录后会生成会话文件（*.tw_session），该文件已被添加到.gitignore中，不会被提交到代码仓库

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
