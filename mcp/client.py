from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai.chat_models.base import BaseChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
import asyncio


# 一：创建聊天和记忆功能
memory = MemorySaver()                                                      # langchain 提供的对话记忆功能
config = {"configurable": {"thread_id": "user1"}}                           # 记忆配置模块，thread_id用于区分不同的对话线程
llm = BaseChatOpenAI(model='deepseek-chat',                                 # langchain接入DeepSeek聊天模型
                     openai_api_key="sk-9cc79d17dec3438e92ef90db423e20c1", 
                     openai_api_base="https://api.deepseek.com") 

# 二：创建MCP Client，接入多个mcp_server
client = MultiServerMCPClient(
    {
        "stdio_1": {
            "command": "python",                            # 运行stdio的mcp工具的命令
            "args": ["./stdio_tools.py"],            # stdio的mcp路径
            "transport": "stdio",                           # stdio方式部署的mcp工具    
        },
        "http_1": {
            "url": "https://server.smithery.ai/@Aas-ee/open-websearch/mcp?api_key=29e17d2f-5e28-4ea1-9199-e142937ac454&profile=juicy-mite-W7YIJ4",               # http的mcp地址
            "transport": "streamable_http",                   # http方式部署的mcp工具
        },
        "http_2": {
            "url": "https://server.smithery.ai/@chenmingkong/bilibili-mcp-server/mcp?api_key=29e17d2f-5e28-4ea1-9199-e142937ac454&profile=juicy-mite-W7YIJ4",               # http的mcp地址
            "transport": "streamable_http",                   # http方式部署的mcp工具
        },
    }
)        

async def main(query):
    tools_list = await client.get_tools()                                       # 获取所有工具
    print("工具列表：", tools_list)                                              # 打印工具列表
    agent = create_react_agent(model=llm,                                       # 接入聊天模型
                               tools=tools_list,                                # 接入工具列表
                               checkpointer=memory)                             # 接入记忆模块
    input_message = {"role": "user", "content": query}                          # 用户输入消息
    messages = {"messages": [input_message]}                                    # 构建消息列表
    step_count = set()                                                          # 记录步骤
    async for chunk in agent.astream(messages, 
                                 config, 
                                 stream_mode="messages"):                        # 异步运行agent           
        content = chunk[0].content                                              # 当前输出内容
        step = chunk[1]["langgraph_step"]                                         # 当前步骤  
        node = chunk[1]["langgraph_node"]                                       # 当前节点
        if content:                                                             # 如果有内容，打印
            if step not in step_count:                                          # 如果是新步骤，打印步骤信息
                step_count.add(step)        
                print(f"\n>> Step {step}: {node}")
            print(content, end='', flush=True)                                  # 打印当前内容


if __name__ == "__main__":
    query = "使用bilibili搜索蓝色战衣相关视频，返回标题，介绍以及视频的地址，搜索5个。"                                      # 用户输入问题
    asyncio.run(main(query))                                                    # 运行异步主函数