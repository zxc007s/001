from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_tools import tools_list
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


# 一：创建聊天和记忆功能
memory = MemorySaver()                                                      # langchain 提供的对话记忆功能
config = {"configurable": {"thread_id": "user1"}}                           # 记忆配置模块，thread_id用于区分不同的对话线程
llm = BaseChatOpenAI(model='deepseek-chat',                                 # langchain接入DeepSeek聊天模型
                     openai_api_key="sk-6bc2fa18c7564779b2cdfcaffa8db9a3", 
                     openai_api_base="https://api.deepseek.com")            

# 二：创建agent
agent = create_react_agent(model=llm,                                       # 接入聊天模型
                           tools=tools_list,                                # 接入工具列表
                           checkpointer=memory)                             # 接入记忆模块

# 三：agent推理
input_message = {"role": "user", "content": "请帮计算两斤苹果，三斤香蕉，3斤西瓜一共多少钱？"}       # 用户输入消息
messages = {"messages": [input_message]}                                    # 构建消息列表
result = agent.stream(messages,                                             # 传入消息
                      config,                                               # 记忆配置
                      stream_mode="messages")                               # 流式输出每一步

# 四：打印结果
step_count = set()                                                          # 记录步骤               
for i, chunk in enumerate(result):
    content = chunk[0].content                                              # 当前输出内容
    step = chunk[1]["langgraph_step"]                                       # 当前步骤  
    node = chunk[1]["langgraph_node"]                                       # 当前节点
    if content:                                                             # 如果有内容，打印
        if step not in step_count:                                          # 如果是新步骤，打印步骤信息
            step_count.add(step)
            print(f"\n>> Step {step}: {node}")
        print(content, end='', flush=True)                                  # 打印当前内容