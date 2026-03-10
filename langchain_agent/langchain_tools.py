from langchain_core.tools import tool
import re
import time
import os
import subprocess
import sys
from openai import OpenAI


# 准备工作：定义工具
@tool
def ask_fruit_unit_price(fruit: str) -> str:
    """
    获取水果的价格
    :param fruit: 水果名称
    :return: 水果的单价信息
    """
    if re.search(r"苹果|apple", fruit):
        return "苹果的单价是10元每公斤"
    elif re.search(r"香蕉|banana", fruit):
        return "香蕉单价为6元每公斤"
    else:
        return "{} 单价为20元每公斤".format(fruit)

@tool
def calculate(what: str) -> float:
    """
    运行计算函数并返回计算结果-使用Python，因此必要时请务必使用浮点语法
    :param what: 要计算的表达式
    :return: 计算结果
    """
    return eval(what)

@tool
def code_write(code: str) -> str:
    """
    将生成的代码进行保存
    :param code: 生成的代码
    :return: 代码保存的路径
    """
    save_path = "../data/code"
    time_current = str(int(time.time()))
    full_path = os.path.join(save_path, time_current + ".py")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return full_path

@tool
def code_execute(full_path: str) -> str:
    """
    代码执行工具，执行Python代码文件。
    :param full_path: 代码保存的路径
    :return: 成功消息
    """
    try:
        cmd = [sys.executable, str(full_path)]
        result = subprocess.run(
            cmd,
            capture_output=True,
        )
        return "代码执行成功。"
    except Exception as e:
        return f"执行过程中发生错误：{str(e)}"
    
@tool
def code_generate(query: str) -> str:
    """
    代码生成工具，可以根据用户的需求生成代码。
    :param query: 用户的需求描述
    :return: 生成的代码
    """
    client = OpenAI(
        api_key="sk-6bc2fa18c7564779b2cdfcaffa8db9a3",
        base_url="https://api.deepseek.com",
    )
    prompt = """
    ## 
    一：你本次的任务是根据用户的输入，生成对应的代码。

    ## 
    二：你的输出必须严格按照我给的模版示例进行输出，请不要输出```python```等格式，只输出代码的内容。

    ##
    三：输出的示例
    用户需求：请帮我写一个Python代码，打印Hello, World!和hello zyh。
    生成的代码：
    print('Hello, World!')
    print('hello zyh')

    ##
    四：用户的需求如下：
    """
    messages = [{"role": "system", "content": "你是一名专业代码生成助手"},
                {"role": "user", "content": prompt + query}]
    response_cg = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )

    result = response_cg.choices[0].message.content              # 获取生成的代码
    return result

tools_list = [ask_fruit_unit_price, calculate, code_write, code_execute, code_generate]

if __name__ == "__main__":
    # code_execute("../data/code/1757491303.py")
    print(ask_fruit_unit_price("苹果"))
    print(ask_fruit_unit_price("香蕉"))
    print(ask_fruit_unit_price("橙子"))
