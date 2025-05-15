from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


def get_llm_response(prompt: str) -> str:
    """
    使用 langchain-openai 调用模型获取响应

    Args:
        prompt (str): 输入的提示词

    Returns:
        str: 模型的完整响应文本
    """
    # 初始化 ChatOpenAI 客户端
    chat = ChatOpenAI(
        model=os.getenv("LLM_API_MODEL"),
        openai_api_base=os.getenv("LLM_API_BASE"),
        openai_api_key=os.getenv("LLM_API_KEY")
    )

    # 创建消息
    messages = [
        SystemMessage(
            content="""
你接下来回答需要严格按照用户要求输出。如果用户要求只返回markdown格式的内容，你就只返回markdown格式的内容，不要添加任何其他的文字。
如果需要分析的内容不符合用户的要求，就返空字符串EMPTY，除此之外不允许返回其它内容。
"""),
        HumanMessage(content=prompt)
    ]

    # 获取响应
    response = chat.invoke(messages)

    return response.content
