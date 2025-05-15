import os
import re
from modules.socialmedia.truthsocial import fetch as fetchTruthsocial
from modules.socialmedia.twitter import fetch as fetchTwitter
from modules.langchain.llm import get_llm_response
from utils.messenger import send
from utils.yaml import load_config_with_env
from dotenv import load_dotenv


load_dotenv()


def main():
    config = load_config_with_env('config/social-networks.yml')

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
                f"在 {account['type']}: {account['socialNetworkId']} 上未发现有更新的内容")
            continue

        for post in posts:
            messenger_variables = post.get_dict()
            prompt = re.sub(r'\$(\w+)', r'{\1}', account['prompt'])
            prompt = prompt.format(**messenger_variables)

            ai_result = get_llm_response(prompt)

            if ai_result == 'EMPTY':
                print(
                    f"在 {account['type']}: {account['socialNetworkId']} 上发现有更新的内容，但内容与需要关注的主题无关: {post_dict['content']}")
                continue

            messenger_variables['ai_result'] = ai_result

            if 'messengers' in account and isinstance(account['messengers'], list):
                for messenger in account['messengers']:
                    # 发送消息
                    send(messenger, messenger_variables)


if __name__ == "__main__":
    main()
