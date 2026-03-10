import time
import os
from mcp.server.fastmcp import FastMCP
import pyautogui


# 初始化mcp实例
mcp = FastMCP("code_generate")


@mcp.tool()
def screen_shot():
    """
    截图工具，截取当前屏幕图像并保存至本地
    :return: 截图结果
    """
    save_path = "../data/images"                                 # 截图保存路径
    time_current = str(time.time())                             # 获取当前时间戳
    full_path = os.path.join(save_path, time_current+".png")    # 拼接完整路径
    try:
        screenshot = pyautogui.screenshot()                     # 截取当前屏幕图像
        screenshot.save(full_path)                              # 保存图像
        return "工具调用成功，截图已保存至: " + full_path         # 返回成功信息
    except Exception as e:
        return f"截图失败: {e}"                                  # 返回错误信息
    

if __name__ == "__main__":
    print("stdio_tools mcp server is running...")
    mcp.run(transport='stdio')