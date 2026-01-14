import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from src.core.policy_engine import engine

# --- New: 引入刚刚写的 LLM 客户端 ---
from src.core.llm import llm_client

app = FastAPI(
    title="LawShield-CN Enterprise Gateway",
    description="策略驱动的中国法律合规 AI 网关",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    query: str
    user_id: str = "anonymous"


class ChatResponse(BaseModel):
    response: str
    is_blocked: bool = False
    blocked_reason: str = None
    legal_ref: str = None


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_query = request.query

    # --- 1. Input Guard (输入拦截) ---
    is_blocked, msg, ref = engine.check_input(user_query)
    if is_blocked:
        return ChatResponse(
            response=msg,
            is_blocked=True,
            blocked_reason="policy_violation",
            legal_ref=ref,
        )

    # --- 2. LLM Call (真实调用) ---
    print(f"🤖 [网关转发] 正在请求大模型: {user_query}")
    ai_response = llm_client.chat(user_query)

    # --- 3. Output Guard (简单输出审计 - Day 3 新增) ---
    # 简单的关键词检查，防止 AI 说出“我不确定”这种不专业的词（演示用）
    if "我不确定" in ai_response:
        ai_response += "\n\n(系统提示：AI回答仅供参考，具体请咨询专业律师。)"

    return ChatResponse(response=ai_response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
