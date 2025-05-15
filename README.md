# Secretary - 社交媒体内容分析助手

## 项目简介

Secretary 是一个自动化的社交媒体分析工具，专门用于监控和分析社交媒体平台上的内容，并通过 AI 进行智能分析。该工具能够自动抓取指定账号的最新发言，根据配置的分析提示词进行内容分析，并将分析结果通过诸如企业微信机器人、个人微信号推送给指定用户。通过灵活配置分析提示词，可以针对不同主题（如财经、政治、科技等）进行定制化分析。

## 主要功能

- 支持多个社交媒体平台的监控（目前支持 Truth Social 和 Twitter）
- 可配置多个监控账号，每个账号可以设置不同的分析提示词
- 支持自定义分析主题和维度，通过配置提示词实现灵活的分析策略
- 使用 AI 进行内容分析，支持任何支持 langchain 规范的 LLM 模型供应商
- 灵活的消息推送支持：
  - 高度自定义配置消息推送通道
  - 每个监控账号可以配置不同的推送目标

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/zkd8907/secretary.git
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

## 配置说明

### 环境变量

环境变量会同时读取系统的环境变量以及项目根目录下的 `.env` 文件。
你可以使用从 `example.env` 复制一份 `.env` 文件并做必要的调整：

```properties
# Redis 配置，用于存储最新处理的消息
REDIS_URL=redis://your_redis_url

# LLM API 配置
LLM_API_MODEL=your_model_name
LLM_API_KEY=your_api_key
LLM_API_BASE=your_api_base_url

# Twitter 配置
# 推荐使用 session 方式登录，session的内容可以在使用用户名密码后从 session.tw_session 文件中获取
# 确保 token 中没有空格，否则将无法正常工作
TWITTER_SESSION=your_twitter_session
# 或者使用用户名密码登录
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password

# Truth Social 配置
# 推荐使用 token 方式登录，token可以在使用用户名密码登录后，从程序的的输出中获取
TRUTHSOCIAL_TOKEN=your_truthsocial_token
# 或者使用用户名密码登录
TRUTHSOCIAL_USERNAME=your_truthsocial_username
TRUTHSOCIAL_PASSWORD=your_truthsocial_password

# 消息推送配置（可选）
# 可以在 .env 中定义这些变量，并在 config/social-networks.yml 中使用
WECOM_TRUMP_ROBOT_URL=your_wecom_robot_webhook_url
WECOM_FINANCE_ROBOT_URL=your_wecom_finance_robot_webhook_url
WECOM_AI_ROBOT_URL=your_wecom_ai_robot_webhook_url
PRIVATE_BARK_URL=your_bark_push_url

# 调试模式（可选）
DEBUG=true
```

### 监控账号配置

创建或修改 `config/social-networks.yml` 文件，配置需要监控的社交媒体账号：

```yaml
social_networks:
  - type: truthsocial
    socialNetworkId: realDonaldTrump
    prompt: >-
      你现在是一名财经专家，请对以下美国总统的发言进行分析，并给按我指定的格式返回分析结果。

      这是你需要分析的内容：$content

      如果需要分析的内容与财经、美股、中美关系、美债市场、科技股或半导体股有关，就按下面的格式输出内容。

      ## Brief Analysis

      分析结果。这部分会展示一个列表，列表中分别包含美股市场、美债市场、科技股、半导体股、中国股票市场、香港股票市场、人民币兑美元汇率、中美关系这8个选项。
      每个选项的值为分别为📈利多和📉利空。如果分析内容对于该选项没有影响，就不要针对这个选项返回任何内容。

      ## Summarize

      这部分需要用非常简明扼要的文字对分析结果进行总结，以及解释为什么在上面针对不同选项会得出不同的结论。
    messengers:
      - url: $WECOM_TRUMP_ROBOT_URL
        method: POST
        headers:
          Content-Type: application/json
        body: >-
          {
              "msgtype": "markdown",
              "markdown": {
                  "content": "# [$poster_name]($poster_url) $post_time

          > $content

          $translation:zh-cn

          $ai_result

          Origin: [$post_url]($post_url)"
              }
          }
      - url: $PRIVATE_BARK_URL
        method: POST
        headers:
          Content-Type: application/json; charset=utf-8
        body: >-
          {
              "title": "$poster_name: $content",
              "group": "finance",
              "url": "$post_url",
              "body": "$ai_result"
          }
  - type: twitter
    socialNetworkId:
      - myfxtrader
      - HAOHONG_CFA
    prompt: >-
      你现在是一名财经专家，请对以下财经博主的发言进行分析，并给按我指定的格式返回分析结果。

      这是你需要分析的内容：$content

      如果需要分析的内容与财经、美股、中美关系、美债市场、科技股或半导体股有关，就按下面的格式输出内容。

      - Summarize

      这部分需要用非常简明扼要的文字对分析结果进行总结，以及解释为什么在上面针对不同选项会得出不同的结论。

      - Brief Analysis

      分析结果。这部分会展示一个列表，列表中分别包含美股市场、美债市场、科技股、半导体股、中国股票市场、香港股票市场、人民币兑美元汇率、中美关系这8个选项。
      每个选项的值为分别为📈利多和📉利空。如果分析内容对于该选项没有影响，就不要针对这个选项返回任何内容。
    messengers:
      - url: $PRIVATE_BARK_URL
        method: POST
        headers:
          Content-Type: application/json; charset=utf-8
        body: >-
          {
              "title": "$poster_name: $content",
              "group": "finance",
              "url": "$post_url",
              "body": "$ai_result"
          }
```

> ⚠️ **重要提示**：
> 
> 1. promptp 字段仅支持 `$content` 变量以及环境变量，不能使用其他内置变量
> 2. 在配置消息推送通道 messengers 时，可以使用以下内置变量：
>    - `$poster_name`: 发布者名称
>    - `$poster_url`: 发布者主页链接
>    - `$post_time`: 发布时间
>    - `$content`: 原始内容
>    - `$translation:zh-cn`: 原始内容翻译为目标语言的内容，目标语言需要符合 [ISO 639-1 标准](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)
>    - `$ai_result`: AI 分析结果
>    - `$post_url`: 原始内容链接
> 3. 配置文件中其它部分的 value 都可以使用 `$` 前缀来引用环境变量，例如：`$WECOM_TRUMP_ROBOT_URL`
> 4. 环境变量只支持任何由大写字母、数字和下划线组成的变量名，不能支持由其他字符构成的环境变量名

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
- 通过配置的企业微信机器人、个人微信推送分析结果

## 输出格式

分析结果将根据配置的消息推送通道进行格式化并发送执行。

## 注意事项

- 确保网络连接正常。Twitter 无法在中国大陆地区访问，Truth Social 无法在中国大陆以及中国香港地区访问。部分云服务商的服务器亦可能会被封锁，导致无法访问 Twitter 和 Truth Social
- Twitter登录后会生成会话文件（*.tw_session），该文件已被添加到.gitignore中，不会被提交到代码仓库

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
