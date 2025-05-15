from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm_response(prompt: str) -> str:
    """
    Get response from the model using langchain-openai

    Args:
        prompt (str): Input prompt

    Returns:
        str: Complete response text from the model
    """

    chat = ChatOpenAI(
        model=os.getenv("LLM_API_MODEL"),
        openai_api_base=os.getenv("LLM_API_BASE"),
        openai_api_key=os.getenv("LLM_API_KEY")
    )

    messages = [
        SystemMessage(
            content="""你接下来回答需要严格按照用户要求输出。如果需要分析的内容不符合用户的要求，就返空字符串EMPTY，除此之外不允许返回其它内容。"""),
        HumanMessage(content=prompt)
    ]

    response = chat.invoke(messages)

    return response.content
