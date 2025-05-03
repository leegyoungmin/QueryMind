from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.controller.mcp_client import MCPClient
import os
import asyncio

app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# 정적 파일 디렉토리 설정
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# MCP 클라이언트 초기화
mcp_client = MCPClient("http://localhost:8000/sse")

@app.get("/")
async def home(request: Request):
    tools = await mcp_client.list_tools()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tools": tools}
    )

@app.get("/tools/{tool_name}")
async def tool_detail(request: Request, tool_name: str):
    tools = await mcp_client.list_tools()
    tool = next((t for t in tools if t.name == tool_name), None)
    if not tool:
        return {"error": "Tool not found"}, 404
    return templates.TemplateResponse(
        "tool.html",
        {"request": request, "tool": tool}
    )

@app.post("/tools/{tool_name}/invoke")
async def invoke_tool(tool_name: str, params: dict):
    result = await mcp_client.invoke_tool(tool_name, params)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 