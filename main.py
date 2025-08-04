import os
import re
from modules.socialmedia.truthsocial import fetch as fetch_truthsocial
from modules.socialmedia.twitter import fetch as fetch_twitter
from modules.langchain.llm import get_llm_response
from utils.messenger import send_message
from utils.yaml import load_config_with_env
from dotenv import load_dotenv


load_dotenv()


def main():
    config = load_config_with_env('config/social-networks.yml')

    network_configs = []
    for network_config in config['social_networks']:
        if isinstance(network_config['socialNetworkId'], list):
            # if socialNetworkId is a list, create a new config for each account ID
            for account_id in network_config['socialNetworkId']:
                if len(account_id) == 0:
                    continue

                account_config = network_config.copy()
                account_config['socialNetworkId'] = account_id
                network_configs.append(account_config)
        else:
            # If not a list, add the original config directly
            network_configs.append(network_config)

    for network_config in network_configs:
        posts = []
        if network_config['type'] == 'truthsocial':
            posts = fetch_truthsocial(network_config['socialNetworkId'])
        if network_config['type'] == 'twitter':
            posts = fetch_twitter(network_config['socialNetworkId'])

        if len(posts) == 0:
            print(
                f"No new post found on {network_config['type']}: {network_config['socialNetworkId']}")
            continue

        for post in posts:
            post_variables = post.get_dict()
            prompt = re.sub(r'\$(\w+)', r'{\1}', network_config['prompt'])
            prompt = prompt.format(**post_variables)

            llm_response = get_llm_response(prompt)

            if llm_response == 'EMPTY':
                print(
                    f"New post found on {network_config['type']}: {network_config['socialNetworkId']}, but it is not related to the topic of interest: {post_variables['content']}")
                continue

            post_variables['ai_result'] = llm_response

            if 'messengers' in network_config and isinstance(network_config['messengers'], list):
                for messenger_config in network_config['messengers']:
                    send_message(messenger_config, post_variables)


if __name__ == "__main__":
    main()
