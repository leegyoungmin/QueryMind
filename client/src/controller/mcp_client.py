from urllib.parse import urlparse
from mcp.client.sse import sse_client
from mcp import ClientSession
from typing import Dict, Any
from src.models.Tool import Tool, ToolParameter, ToolInvokeResult

class MCPClient:
    def __init__(self, endpoint: str):
        if urlparse(endpoint).scheme not in ['http', 'https']:
            raise ValueError("Invalid endpoint: must start with http:// or https://")
        
        self.endpoint = endpoint

    async def list_tools(self):
        tools = []

        async with sse_client(self.endpoint) as stream:
            async with ClientSession(*stream) as session:
                await session.initialize()

                tool_response = await session.list_tools()
                tool_dict = dict(tool_response)
                tool_results = tool_dict.get("tools", [])

                for tool in tool_results:
                    params = []
                    required_params = tool.inputSchema.get("required", [])

                    for param, param_schema in tool.inputSchema.get("properties", {}).items():
                        params.append(
                            ToolParameter(
                                name = param,
                                parameter_type = param_schema.get("type", "string"),
                                description = param_schema.get("description", ""),
                                required = param in required_params,
                                default = param_schema.get("default")
                            )
                        )

                    tools.append(
                        Tool(
                            name = tool.name,
                            description = tool.description,
                            parameters = params,
                            metadata = {
                                "endpoint": self.endpoint,
                            },
                            identifier = tool.name
                        )
                    )

        return tools
    

    async def invoke_tool(self, tool_name: str, kwargs: Dict[str, Any]) -> ToolInvokeResult:
        async with sse_client(self.endpoint) as stream:
            async with ClientSession(*stream) as session:
                await session.initialize()

                result = await session.call_tool(tool_name, kwargs)
                
        return ToolInvokeResult(
            content = "\n".join([result.model_dump_json() for result in result.content]),
            error_code = 1 if result.isError else 0
        )