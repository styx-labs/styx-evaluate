from langchain_openai.chat_models.base import BaseChatOpenAI
from agent.get_secret import get_secret

llm = BaseChatOpenAI(
    model="deepseek-reasoner",
    openai_api_key=get_secret("deepseek-api-key", "1"),
    openai_api_base="https://api.deepseek.com",
    max_tokens=1024,
)
