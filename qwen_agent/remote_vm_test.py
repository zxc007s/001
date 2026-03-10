import asyncio
from openai import AsyncOpenAI
from fastmcp import Client
import json

async def query_mcp_tool(tool_name: str, params: dict):
    """
    调用MCP工具的统一入口
    :param tool_name: 工具名称
    :param params: 工具参数
    :return: 工具执行结果
    """
    async with Client("http://127.0.0.1:4200/demo") as client:
        return await client.call_tool(tool_name, params)

async def chat_with_tools():
    """
    实现支持工具调用的聊天功能
    1. 连接本地vLLM服务
    2. 获取可用工具列表并转换为OpenAI函数调用格式
    3. 根据用户问题调用适当工具
    4. 整合工具结果生成最终回复
    """
    # 连接本地部署的vLLM服务（兼容OpenAI API）
    llm_client = AsyncOpenAI(
        base_url="http://192.168.2.182:8000/v1",
        api_key="EMPTY"  # 本地服务不需要API密钥
    )

    # 动态获取MCP服务提供的工具列表
    async with Client("http://127.0.0.1:4200/demo") as mcp_client:
        tools = await mcp_client.list_tools()
        
        # 将MCP工具模式转换为OpenAI函数调用格式
        tool_schemas = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": tool.inputSchema.get("type", "object"),
                    "properties": {
                        prop_name: prop_def 
                        for prop_name, prop_def in tool.inputSchema["properties"].items()
                    },
                    "required": tool.inputSchema.get("required", [])
                }
            }
        } for tool in tools]

    # 用户提问示例
    user_query = "查询北京天气和贵州茅台股价"
    
    # 第一次调用模型，允许模型决定是否需要调用工具
    response = await llm_client.chat.completions.create(
        model="/data/model",
        messages=[{"role": "user", "content": user_query}],
        tools=tool_schemas,
        tool_choice="auto"  # 让模型自动选择工具
    )

    # 处理工具调用请求
    message = response.choices[0].message
    print(message.tool_calls)
    
    if message.tool_calls:
        print("检测到工具调用请求:")
        
        # 按顺序执行模型请求的所有工具
        if message.tool_calls:
            for call in message.tool_calls:
                print(f"正在执行 {call.function.name}...")
                # 安全解析参数
                arguments = json.loads(call.function.arguments)   # 替换 eval
                result = await query_mcp_tool(call.function.name, arguments)
                print(f"工具返回: {result}")

        # 第二次调用模型，结合工具结果生成最终回复
        final_response = await llm_client.chat.completions.create(
            model="/data/model",  # 使用本地模型路径
            messages=[
                {"role": "user", "content": user_query},  # 原始问题
                message,  # 模型的工具调用计划
                *[{  # 每个工具的执行结果
                    "role": "tool",
                    "name": call.function.name,
                    "content": str(result)
                } for call in message.tool_calls]
            ]
        )
        print("\n最终回复:", final_response.choices[0].message.content)
    else:
        # 如果模型认为不需要工具，直接返回模型回复
        print("直接回复:", message.content)

if __name__ == "__main__":
    # 运行异步聊天函数
    asyncio.run(chat_with_tools())