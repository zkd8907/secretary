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

    # 处理socialNetworkId为数组的情况
    new_social_networks = []
    for account in config['social_networks']:
        if isinstance(account['socialNetworkId'], list):
            # 如果socialNetworkId是数组,为每个ID创建一个新的配置
            for social_id in account['socialNetworkId']:
                if len(social_id) == 0:
                    continue

                new_account = account.copy()
                new_account['socialNetworkId'] = social_id
                new_social_networks.append(new_account)
        else:
            # 如果不是数组直接添加原配置
            new_social_networks.append(account)

    # 用新的配置替换原配置
    config['social_networks'] = new_social_networks

    for account in config['social_networks']:
        posts = []
        if account['type'] == 'truthsocial':
            posts = fetchTruthsocial(account['socialNetworkId'])
        if account['type'] == 'twitter':
            posts = fetchTwitter(account['socialNetworkId'])

        if len(posts) == 0:
            print(
                f"未找到 {account['type']}: {account['socialNetworkId']} 有更新发布的内容")
            continue

        for post in posts:
            content = post.content
            prompt = account['prompt'].format(content=content)
            format_result = None
            rawData = ''

            # 在某些情况下，LLM会返回一些非法的json字符串，所以这里需要循环尝试，直到解析成功为止
            while format_result is None:
                if len(rawData) > 0:
                    prompt += """
你前次基于上面的内容提供给我的json是{rawData}，然而这个json内容有语法错误，无法在python中被解析。针对这个问题重新检查我的要求，按指定要求和格式回答。
"""
                rawData = get_hunyuan_response(prompt).replace('\n', '\\n')
                try:
                    format_result = json.loads(rawData)
                except Exception as e:
                    print(f"解析 JSON 时出错: {e}")
                    print(f"翻译内容: {rawData}")
                    format_result = None

            post_time = post.get_local_time()

            if format_result['is_relevant'] == '0':
                print(
                    f"在 {post_time.strftime('%Y-%m-%d %H:%M:%S')} 未发现相关内容: {content}")
                continue

            markdown_msg = f"""# [{post.poster_name}]({post.poster_url}) {post_time.strftime('%Y-%m-%d %H:%M:%S')}


{format_result['analytical_briefing']}


origin: [{post.url}]({post.url})"""

            send_markdown_msg(
                markdown_msg,
                os.getenv(account['weComRobotEnvName'], '')
            )


if __name__ == "__main__":
    main()
