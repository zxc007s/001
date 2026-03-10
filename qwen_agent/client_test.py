import asyncio
import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def test_mcp_service():
    SERVICE_URL = "http://127.0.0.1:4200/demo"
    
    try:
        transport = StreamableHttpTransport(url=SERVICE_URL)
        async with Client(transport) as client:
            print(f"成功连接到MCP服务: {SERVICE_URL}")
            await client.ping()
            print("服务心跳检测成功")
            
            tools = await client.list_tools()
            tool_names = [tool.name for tool in tools]
            print(f"可用工具列表: {', '.join(tool_names)}")
            
            # 测试天气工具
            print("\n" + "="*30)
            print("测试天气工具")
            print("="*30)
            
            weather_result = await client.call_tool("weather", {"city": "北京"})
            # 直接使用 data 属性访问结构化数据
            if weather_result.data:
                print(f"北京天气: 温度={weather_result.data.get('temp')}℃, 天气={weather_result.data.get('condition')}")
            
            # 测试股票工具
            print("\n" + "="*30)
            print("测试股票工具")
            print("="*30)
            
            stock_result = await client.call_tool("stock", {"code": "512605"})
            if stock_result.data:
                print(f"股票查询: 名称={stock_result.data.get('name', '未知')}, 价格={stock_result.data.get('price', '未知')}")
            
            # 测试错误处理
            print("\n" + "="*30)
            print("测试错误处理")
            print("="*30)
            
            error_result = await client.call_tool("weather", {"city": "东京"})
            if error_result.data and 'error' in error_result.data:
                print(f"错误信息: {error_result.data['error']}")
    
    except httpx.ConnectError:
        print(f"连接失败！请检查服务是否运行在 {SERVICE_URL}")
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    print("="*50)
    print("FastMCP服务测试脚本")
    print("="*50)
    asyncio.run(test_mcp_service())