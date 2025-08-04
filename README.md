# Secretary - Social Media Content Analysis Assistant

[简体中文](README-zh.md) ｜ English

## Project Overview

Secretary is an automated social media analysis tool designed to monitor and analyze content across social media platforms using AI-powered analysis. The tool automatically fetches the latest posts from specified accounts, analyzes the content based on configured prompts, and delivers the analysis results to designated users through channels such as WeChat Work bots and personal WeChat accounts. Through flexible prompt configuration, it enables customized analysis for different topics (such as finance, politics, technology, etc.).

## Key Features

- Support for multiple social media platforms (currently Truth Social and Twitter)
- Configurable monitoring accounts with customizable analysis prompts
- Customizable analysis topics and dimensions through prompt configuration
- AI-powered content analysis supporting any LLM model provider compatible with langchain specifications
- Flexible message delivery support:
  - Highly customizable message delivery channels
  - Different delivery targets configurable for each monitored account

## Installation Guide

1. Clone the repository:
```bash
git clone https://github.com/zkd8907/secretary.git
cd secretary
```

2. Install and configure uv (recommended):
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies using uv
uv sync
```

Or use traditional venv method (not recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
pip install -e .
```

## Configuration Guide

### Environment Variables

Environment variables are read from both system environment variables and the `.env` file in the project root directory.
You can copy `example.env` to create your `.env` file and make necessary adjustments:

```properties
# Redis configuration for storing latest processed messages
REDIS_URL=redis://your_redis_url

# LLM API configuration
LLM_API_MODEL=your_model_name
LLM_API_KEY=your_api_key
LLM_API_BASE=your_api_base_url

# Twitter configuration
# Recommended to use session-based login, session content can be obtained from session.tw_session file after using username/password
# Ensure there are no spaces in the token, otherwise it won't work properly
TWITTER_SESSION=your_twitter_session
# Or use username/password login
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password

# Truth Social configuration
# Recommended to use token-based login, token can be obtained from program output after username/password login
TRUTHSOCIAL_TOKEN=your_truthsocial_token
# Or use username/password login
TRUTHSOCIAL_USERNAME=your_truthsocial_username
TRUTHSOCIAL_PASSWORD=your_truthsocial_password

# Message delivery configuration (optional)
# These variables can be defined in .env and used in config/social-networks.yml
WECOM_TRUMP_ROBOT_URL=your_wecom_robot_webhook_url
WECOM_FINANCE_ROBOT_URL=your_wecom_finance_robot_webhook_url
WECOM_AI_ROBOT_URL=your_wecom_ai_robot_webhook_url
PRIVATE_BARK_URL=your_bark_push_url

# Debug mode (optional)
DEBUG=true

# Scheduler configuration (optional)
SCHEDULE_INTERVAL_MINUTES=5
RUN_ON_START=false
```

### Account Monitoring Configuration

Create or modify the `config/social-networks.yml` file to configure social media accounts for monitoring:

```yaml
social_networks:
  - type: truthsocial
    socialNetworkId: realDonaldTrump
    prompt: >-
      You are now a financial expert. Please analyze the following statement from the US President and return the analysis results in the specified format.

      This is the content you need to analyze: $content

      If the content is related to finance, US stocks, US-China relations, US bond market, tech stocks, or semiconductor stocks, output the content in the following format.

      ## Brief Analysis

      Analysis results. This section will display a list containing US stock market, US bond market, tech stocks, semiconductor stocks, Chinese stock market, Hong Kong stock market, USD/CNY exchange rate, and US-China relations.
      Each option's value should be either 📈 Bullish or 📉 Bearish. If the analysis content has no impact on an option, do not include that option in the output.

      ## Summarize

      This section should provide a very concise summary of the analysis results and explain why different conclusions were reached for different options above.
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
      You are now a financial expert. Please analyze the following statement from the financial blogger and return the analysis results in the specified format.

      This is the content you need to analyze: $content

      If the content is related to finance, US stocks, US-China relations, US bond market, tech stocks, or semiconductor stocks, output the content in the following format.

      - Summarize

      This section should provide a very concise summary of the analysis results and explain why different conclusions were reached for different options above.

      - Brief Analysis

      Analysis results. This section will display a list containing US stock market, US bond market, tech stocks, semiconductor stocks, Chinese stock market, Hong Kong stock market, USD/CNY exchange rate, and US-China relations.
      Each option's value should be either 📈 Bullish or 📉 Bearish. If the analysis content has no impact on an option, do not include that option in the output.
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

> ⚠️ **Important Notes**:
> 
> 1. The prompt field only supports the `$content` variable and environment variables, other built-in variables cannot be used
> 2. When configuring message delivery channels (messengers), the following built-in variables can be used:
>    - `$poster_name`: Publisher's name
>    - `$poster_url`: Publisher's profile URL
>    - `$post_time`: Post time
>    - `$content`: Original content
>    - `$translation:zh-cn`: Original content translated to target language, target language must comply with [ISO 639-1 standard](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)
>    - `$ai_result`: AI analysis result
>    - `$post_url`: Original content URL
> 3. Other parts of the configuration file can use environment variables with `$` prefix, e.g.: `$WECOM_TRUMP_ROBOT_URL`
> 4. Environment variables only support names consisting of uppercase letters, numbers, and underscores, other characters are not supported

## Usage

1. Ensure environment variables and monitoring accounts are properly configured

2. **Scheduled execution (recommended)**:
```bash
# Run with built-in scheduler (default 5-minute intervals)
python scheduler.py

# Or with custom interval (10 minutes)
SCHEDULE_INTERVAL_MINUTES=10 python scheduler.py

# Or using Docker
docker run -e SCHEDULE_INTERVAL_MINUTES=10 your-image
```

3. **Single execution**:
```bash
python main.py
```

The program will automatically:

- Fetch the latest posts from configured social media accounts
- Perform AI analysis and translation based on each account's configured prompts
- Generate analysis reports
- Deliver analysis results through configured WeChat Work bots and personal WeChat accounts

### Scheduler Configuration

- `SCHEDULE_INTERVAL_MINUTES`: Execution interval in minutes (default: 5)
- `RUN_ON_START`: Whether to run immediately on startup (default: false)

## Output Format

Analysis results will be formatted and delivered according to the configured message delivery channels.

## Notes

- Ensure stable network connection. Twitter is not accessible in mainland China, and Truth Social is not accessible in mainland China and Hong Kong. Some cloud service providers' servers may also be blocked, preventing access to Twitter and Truth Social
- Twitter login will generate a session file (*.tw_session), which has been added to .gitignore and will not be committed to the code repository

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
