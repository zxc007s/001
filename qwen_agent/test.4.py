import asyncio
import json
import re  # 新增
from openai import AsyncOpenAI
from fastmcp import Client

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

    response = await llm_client.chat.completions.create(
        model="/data/model",  # 注意去掉末尾斜杠
        messages=[{"role": "user", "content": user_query}],
        tools=tool_schemas,
        tool_choice="auto"
    )

    message = response.choices[0].message
    content = message.content

    # 尝试解析 XML 格式的工具调用
    tool_calls = []
    if content and "<tool_call>" in content:
        # 使用正则提取 <tool_call> 标签内的内容
        pattern = r'<tool_call>\s*(.*?)\s*</tool_call>'
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            try:
                call_data = json.loads(match)
                tool_calls.append({
                    "function": {
                        "name": call_data["name"],
                        "arguments": json.dumps(call_data["arguments"])
                    }
                })
            except:
                pass

    if tool_calls:
        print("检测到工具调用请求 (从 XML 解析):")
        for call in tool_calls:
            func_name = call["function"]["name"]
            arguments = json.loads(call["function"]["arguments"])
            print(f"正在执行 {func_name}...")
            result = await query_mcp_tool(func_name, arguments)
            print(f"工具返回: {result}")

        # 第二次调用，将工具结果传回模型
        final_response = await llm_client.chat.completions.create(
            model="/data/model",
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": content},  # 原始回复包含 XML
                *[{
                    "role": "tool",
                    "name": call["function"]["name"],
                    "content": str(result)
                } for call in tool_calls]
            ]
        )
        print("\n最终回复:", final_response.choices[0].message.content)
    else:
        print("直接回复:", content)


if __name__ == "__main__":
    # 运行异步聊天函数
    asyncio.run(chat_with_tools())