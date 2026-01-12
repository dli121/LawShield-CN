import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 初始化 FastAPI 应用
# title 和 description 会自动生成漂亮的 API 文档
app = FastAPI(
    title="LawShield-CN Enterprise Gateway",
    description="策略驱动的中国法律合规 AI 网关 (Policy-Driven AI Governance)",
    version="0.1.0"
)

# 定义请求的数据模型 (Schema)
# 这体现了你的接口规范意识
class ChatRequest(BaseModel):
    query: str  # 用户的问题
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    is_blocked: bool = False
    blocked_reason: str = None

# --- 核心路由 ---

@app.get("/")
def health_check():
    """健康检查接口：用于 K8s 或监控系统检测服务是否存活"""
    return {"status": "running", "system": "LawShield-CN"}

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    模拟网关处理流程：
    User -> [Input Guard] -> LLM -> [Output Guard] -> User
    """
    user_query = request.query
    
    # --- 1. 模拟 Input Guard (明天我们要实现真的逻辑) ---
    print(f"收到请求: {user_query}")
    
    # 简单的硬编码拦截演示
    if "洗钱" in user_query:
        return ChatResponse(
            response="【安全拦截】您的提问触发了《反洗钱法》合规限制，已终止处理。",
            is_blocked=True,
            blocked_reason="legal_compliance_finance"
        )
    
    # --- 2. 模拟调用 LLM (Mock) ---
    # 暂时不真的调 OpenAI，先假装生成一个回答
    ai_response = f"这是 AI 对 '{user_query}' 的模拟回答。"
    
    # --- 3. 返回结果 ---
    return ChatResponse(response=ai_response)

# 启动入口
if __name__ == "__main__":
    # 使用 uvicorn 启动服务，端口 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)