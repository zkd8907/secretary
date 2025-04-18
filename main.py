import json
import yaml
import sys
from modules.socialmedia.truthsocial import fetch as fetchTruthsocial
from modules.socialmedia.twitter import fetch as fetchTwitter
from modules.langchain.hunyuan import get_hunyuan_response
from modules.wecom import send_markdown_msg
from dotenv import load_dotenv
import os

load_dotenv()


def load_config():
    config_path = 'config/social-networks.yml'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"错误：配置文件 {config_path} 不存在")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"错误：配置文件格式不正确: {e}")
        sys.exit(1)


def main():
    config = load_config()

    for account in config['social_networks']:
        posts = []
        if account['type'] == 'truthsocial':
            posts = fetchTruthsocial(account['socialNetworkId'])
        if account['type'] == 'twitter':
            posts = fetchTwitter(account['socialNetworkId'])

        if len(posts) == 0:
            print(f"未找到 {account['type']}: {account['socialNetworkId']} 的帖子")
            continue

        for post in posts:
            content = post.content
            prompt = account['prompt'].format(content=content)
            format_result = None

            # 在某些情况下，LLM会返回一些非法的json字符串，所以这里需要循环尝试，直到解析成功为止
            while format_result is None:
                translated = get_hunyuan_response(prompt)
                try:
                    format_result = json.loads(
                        translated.replace('\n', '\\n'))
                except Exception as e:
                    print(f"解析 JSON 时出错: {e}")
                    print(f"翻译内容: {translated}")
                    format_result = None

            post_time = post.post_on

            if format_result['is_relevant'] == '0':
                print(
                    f"在 {post_time.strftime('%Y-%m-%d %H:%M:%S')} 未发现相关内容: {content}")
                continue

            markdown_msg = f"""# {post_time.strftime('%Y-%m-%d %H:%M:%S')}

{format_result['analytical_briefing']}"""

            if 'footer' in account and len(account['footer']) > 0:
                markdown_msg += f"\n\n{account['footer']}"

            send_markdown_msg(
                markdown_msg,
                os.getenv(account['weComRobotEnvName'], '')
            )


if __name__ == "__main__":
    main()
