import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件里的配置
load_dotenv()


class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL")
        )
        self.model = os.getenv("LLM_MODEL", "gpt-4o")
        print(f"🔌 [LLMClient] 已连接至: {self.model}")

    def chat(self, user_query: str) -> str:
        """
        发送请求给大模型，并获取回复
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    # System Prompt: 设定 AI 的人设，这在治理中也很重要
                    {
                        "role": "system",
                        "content": "你是一个专业的法律合规助手。回答需严谨、客观。",
                    },
                    {"role": "user", "content": user_query},
                ],
                temperature=0.3,  # 温度低一点，回答更严谨
                max_completion_tokens=500,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ [LLM Error] 调用失败: {e}")
            return "对不起，AI 服务暂时不可用，请稍后再试。"


# 单例模式
llm_client = LLMClient()
