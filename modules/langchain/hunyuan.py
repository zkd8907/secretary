from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
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
    messages = [HumanMessage(content=prompt)]

    # 获取响应
    response = chat.invoke(messages)

    return response.content
