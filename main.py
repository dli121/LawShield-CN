import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# --- New: 引入我们写的引擎 ---
from src.core.policy_engine import engine 

app = FastAPI(
    title="LawShield-CN Enterprise Gateway",
    description="策略驱动的中国法律合规 AI 网关",
    version="0.1.0"
)

class ChatRequest(BaseModel):
    query: str
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    is_blocked: bool = False
    blocked_reason: str = None
    legal_ref: str = None # --- New: 增加法条返回字段

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_query = request.query
    
    # --- New: 使用策略引擎进行检查 ---
    # 不再是写死的 if else，而是动态加载 yaml 规则
    is_blocked, msg, ref = engine.check_input(user_query)
    
    if is_blocked:
        return ChatResponse(
            response=msg,
            is_blocked=True,
            blocked_reason="policy_violation",
            legal_ref=ref
        )
    
    # 如果通过检查，这里模拟 AI 回答
    ai_response = f"LawShield: 您的提问符合合规要求。AI正在思考：{user_query}..."
    return ChatResponse(response=ai_response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)