from mcp.server.fastmcp import FastMCP
import re
import requests


# 初始化mcp实例
mcp = FastMCP("http_1", port=8022, host = "0.0.0.0")


@mcp.tool()
async def ask_fruit_unit_price(fruit: str) -> str:
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

@mcp.tool()
async def calculate(what: str) -> float:
    """
    运行计算函数并返回计算结果-使用Python，因此必要时请务必使用浮点语法
    :param what: 要计算的表达式
    :return: 计算结果
    """
    return eval(what)

@mcp.tool()
async def weather_index(city:str) -> dict:
    """
    天气查询工具, 获取给定城市的天气信息，根据城市编号进行查询
    :param city: 城市编号
    :return: 天气信息
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"  # 天气查询api请求地址
    api_key = "e508c9ba8eea226895dc263f418f8653"                # 天气查询api请求apikey
    params = {
        "key": api_key,
        "city": city,
    }                                                           # 请求参数
    try:
        response = requests.get(url, params=params)             # 发送请求
        weather_data = response.json()           
        return weather_data['lives'][0]                         # 获取请求得到的数据，并返回
    except Exception as e:
        return e                                                # 打印错误信息


if __name__ == "__main__":
    mcp.run(transport='streamable-http')
