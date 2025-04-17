import datetime
import json
from modules.truthsocial.main import fetch as fetchTruthsocial
from modules.langchain.hunyuan import get_hunyuan_response
from modules.wecom import send_markdown_msg
from dotenv import load_dotenv
import os

load_dotenv()

PROMPT = """你现在是一名精通英文的财经专家，请对以下美国总统的发言进行分析，并给按我指定的格式返回分析结果。输出格式为原始的json字符串。在最终输出中，除了json字符串本身的内容，不需要其它信息。同时返回的json也不需要以markdown格式返回。

内容：{content}

输出格式：
{{
    "origin": "原文内容",
    "translated": "翻译结果",
    "effects": {{
        "美股市场": "对于美国股票市场的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "美债市场": "对于美国债券市场的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "科技股": "对于美国科技股的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "半导体股": "对于半导体股的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "中国股票市场": "对于中国股票市场的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "香港股票市场": "对于香港股票市场的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "美元汇率": "对于美元兑人民币汇率的影响，只需要返回Positive, Negative, Neutral这三个值之一即可",
        "中美关系": "对于中美关系的影响，只需要返回Positive, Negative, Neutral这三个值之一即可"
    }}
}}
"""

EFFECTS = {
    "Positive": "📈利多",
    "Negative": "📉利空",
}


def main():
    posts = fetchTruthsocial("realDonaldTrump")

    if len(posts) == 0:
        print("No posts found")
        return

    for post in posts:
        content = post['content']
        prompt = PROMPT.format(content=content)
        translated = get_hunyuan_response(prompt)
        format_result = json.loads(translated)
        effects = []
        for effect in format_result['effects']:
            if format_result['effects'][effect] == "Neutral":
                continue

            effects.append(
                f"{effect}: {EFFECTS[format_result['effects'][effect]]}")

        post_time = datetime.datetime.strptime(
            post['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        post_time = post_time + datetime.timedelta(hours=8)
        post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

        if len(effects) == 0:
            print(f"No effects found for {post_time}: {content}")
            continue

        markdown_msg = f"""# {post_time}


> {format_result['origin']}
        

{format_result['translated']}


## Brief Analysis


{effects}"""

        send_markdown_msg(markdown_msg, os.getenv('WECOM_ROBOT_ID'))


if __name__ == "__main__":
    main()
