from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


def get_hunyuan_response(prompt: str) -> str:
    """
    使用 langchain-openai 调用 hunyuan-turbos-latest 模型获取响应

    Args:
        prompt (str): 输入的提示词

    Returns:
        str: 模型的完整响应文本
    """
    # 初始化 ChatOpenAI 客户端
    chat = ChatOpenAI(
        model="hunyuan-turbos-latest",
        openai_api_base=os.getenv("HUNYUAN_API_BASE"),
        openai_api_key=os.getenv("HUNYUAN_API_KEY")
    )

    # 创建消息
    messages = [
        SystemMessage(
            content="""
你接下来回答的所有内容都只能是符合我要求的json字符串同。
字符串中如果有一些特殊的字符需要做好转义，确保最终这个json字符串可以在python中被正确解析。
在最终的回答中除了json字符串本身，不需要其它额外的信息，也不要在json内容前后额外增加markdown的三个点转义。
"""),
        HumanMessage(content=prompt)
    ]

    # 获取响应
    response = chat.invoke(messages)

    return response.content
