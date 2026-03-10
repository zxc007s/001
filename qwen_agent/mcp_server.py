from fastmcp import FastMCP

# 创建FastMCP应用实例，"demo"为应用名称
app = FastMCP("demo")

# 注册天气查询工具，用于获取指定城市的天气信息
@app.tool(name="weather", description="城市天气查询")
def get_weather(city: str):
    # 预设的天气数据（实际应用中可替换为API调用）
    weather_data = {
        "北京": {"temp": 25, "condition": "晴"},
        "上海": {"temp": 28, "condition": "多云"}
    }
    # 返回对应城市的天气，不存在则返回错误信息
    return weather_data.get(city, {"error": "未找到该城市"})

# 注册股票查询工具，用于获取指定股票代码的价格信息
@app.tool(name="stock", description="股票价格查询")
def get_stock(code: str):
    # 预设的股票数据（实际应用中可替换为API调用）
    stock_data = {
        "600519": {"name": "贵州茅台", "price": 1825.0},
        "000858": {"name": "五粮液", "price": 158.3}
    }
    # 返回对应股票的信息，不存在则返回错误信息
    return stock_data.get(code, {"error": "未找到该股票"})

if __name__ == "__main__":
    # 启动HTTP服务，支持流式响应
    app.run(
        transport="streamable-http",  # 使用支持流式传输的HTTP协议
        host="127.0.0.1",            # 监听本地地址
        port=4200,                   # 服务端口
        path="/demo",                # 服务路径前缀
        log_level="debug",           # 调试日志级别
    )