import json
from modules.socialmedia.truthsocial import fetch as fetchTruthsocial
from modules.langchain.hunyuan import get_hunyuan_response
from modules.wecom import send_markdown_msg
from dotenv import load_dotenv
import os

load_dotenv()

PROMPT = """你现在是一名财经专家，请对以下{poster}的发言进行分析，并给按我指定的格式返回分析结果。
输出格式为原始合法的json字符串，字符串中如果有一些特殊的字符需要做好转义，确保最终这个json字符串可以在python中被正确解析。
在最终输出的内容中除了json字符串本身，不需要其它额外的信息，也不要在json内容前后额外增加markdown的三个点转义。

这是你需要分析的内容：{content}

这是输出格式的说明：
{{
    "is_relevant": "是否与财经相关，只需要返回1或0这两个值之一即可",
    "analytical_briefing: "分析简报"
}}

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
"""


def main():
    posts = fetchTruthsocial("realDonaldTrump")

    if len(posts) == 0:
        print("No posts found")
        return

    for post in posts:
        content = post.content
        prompt = PROMPT.format(content=content, poster='美国总统特朗普')
        format_result = None

        # 在某些情况下，LLM会返回一些非法的json字符串，所以这里需要循环尝试，直到解析成功为止
        while format_result is None:
            translated = get_hunyuan_response(prompt)
            try:
                format_result = json.loads(translated.replace('\n', '\\n'))
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                print(f"Translated content: {translated}")
                format_result = None

        if format_result['is_relevant'] == '0':
            print(
                f"No effects found for {post.post_on.strftime('%Y-%m-%d %H:%M:%S')}: {content}")
            continue

        markdown_msg = f"""# {post.post_on.strftime('%Y-%m-%d %H:%M:%S')}

{format_result['analytical_briefing']}
"""

        send_markdown_msg(markdown_msg, os.getenv('WECOM_ROBOT_ID'))


if __name__ == "__main__":
    main()
