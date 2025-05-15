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

    social_networks_list = []
    for social_network in config['social_networks']:
        if isinstance(social_network['socialNetworkId'], list):
            # if socialNetworkId is a list, create a new config for each elements in socialNetworkId
            for social_id in social_network['socialNetworkId']:
                if len(social_id) == 0:
                    continue

                new_account = social_network.copy()
                new_account['socialNetworkId'] = social_id
                social_networks_list.append(new_account)
        else:
            # If not a list, add the original config directly
            social_networks_list.append(social_network)

    for social_network in social_networks_list:
        posts = []
        if social_network['type'] == 'truthsocial':
            posts = fetchTruthsocial(social_network['socialNetworkId'])
        if social_network['type'] == 'twitter':
            posts = fetchTwitter(social_network['socialNetworkId'])

        if len(posts) == 0:
            print(
                f"No new post found on {social_network['type']}: {social_network['socialNetworkId']}")
            continue

        for post in posts:
            messenger_variables = post.get_dict()
            prompt = re.sub(r'\$(\w+)', r'{\1}', social_network['prompt'])
            prompt = prompt.format(**messenger_variables)

            ai_result = get_llm_response(prompt)

            if ai_result == 'EMPTY':
                print(
                    f"New post found on {social_network['type']}: {social_network['socialNetworkId']}, but it is not related to the topic of interest: {messenger_variables['content']}")
                continue

            messenger_variables['ai_result'] = ai_result

            if 'messengers' in social_network and isinstance(social_network['messengers'], list):
                for messenger in social_network['messengers']:
                    send(messenger, messenger_variables)


if __name__ == "__main__":
    main()
