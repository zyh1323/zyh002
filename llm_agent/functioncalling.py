import pyautogui
import time
from openai import OpenAI
import json
import requests


# 定义工具：截图工具，截取当前屏幕，并保存到指定路径。
def screen_shot(save_path):
    try:
        screenshot = pyautogui.screenshot()  # 截取当前屏幕
        screenshot.save(save_path)           # 保存截图到指定路径
        return "工具调用成功，截图已保存到：" + save_path
    except Exception as e:
        return "工具调用失败，错误信息：" + str(e)

# 定义工具：将文本文件，并保存
def write_txt(text):
    try:
        time_current = str(int(time.time()))          # 获取当前时间戳
        file_name = "../data/txt/" + time_current + ".txt"  # 构建文件名
        with open(file_name, "w", encoding="utf-8") as f:  # 打开文件
            f.write(text)                               # 写入文本
        return "工具调用成功，文本已写入并保存。"
    except Exception as e:
        return "工具调用失败，错误信息：" + str(e)

# 定义工具：天气查询工具
def weather_index(city:str):
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


# 定义工具列表：存放工具的使用说明，供大模型使用
tools_list = [
    {"type": "function",                               
     "function": {
         "name": "screen_shot",                             # 这个工具的函数名
         "description": "截取当前屏幕，并保存到指定路径。",   # 工具的描述
         "parameters": {
             "type": "object",
             "properties": {
                "save_path": {                              # 参数一的名字
                     "type": "string",                      # 参数一的类型
                     "description": "保存截图的路径"         # 参数一的描述
                    }
                },      
             "required": ["save_path"]                      # 必须的参数列表
            }   
        }
    },
    {"type": "function",                                 
     "function": {
         "name": "write_txt",                              # 这个工具的函数名
         "description": "写入文本，并保存",                 # 工具的描述
         "parameters": {
             "type": "object",
             "properties": {
                "text": {                                   # 参数一的名称
                     "type": "string",                      # 参数一的类型
                     "description": "需要写入的文本"         # 参数一的描述
                    }
                },      
             "required": ["text"]                           # 必须的参数列表
            }   
        }
    },
    {"type": "function",                                 
     "function": {
         "name": "weather_index",                              # 这个工具的函数名
         "description": "查询指定城市的天气啊，根据城市编号查询。",  # 工具的描述
         "parameters": {
             "type": "object",
             "properties": {
                "city": {                                   # 参数一的名称
                     "type": "string",                      # 参数一的类型
                     "description": "城市编号"              # 参数一的描述
                    }
                },      
             "required": ["city"]                           # 必须的参数列表
            }   
        }
    }
]

# 准备大模型，api调用的方式
url = "https://api.deepseek.com"                  # DeepSeek的API地址
api_key = "sk-9cc79d17dec3438e92ef90db423e20c1"   # DeepSeek的API密钥
model_name = "deepseek-chat"                      # DeepSeek的模型名称
client = OpenAI(api_key=api_key, base_url=url)    # 简历连接
messages = []                                     # 消息列表


# 一.感知： LLM接收用户的输入
query = "请帮我查询山西太原的天气，城市编号：140100"                       # 用户输入的内容
message = {"role": "user", "content": query}      # 构建消息
messages.append(message)                          # 将用户输入添加到消息列表
response = client.chat.completions.create(
    model = model_name,                           # 模型名称      
    messages = messages,                          # 消息列表
    tools = tools_list                            # 提供工具列表
)
print("\n第一次回复：", response, "\n\n")          # 打印模型的回复

# 二.规划：决定要调用哪一个函数，以及函数的参数。
if response.choices[0].message.tool_calls:                  # 如果需要调用工具，执行下面的流程
    result = response.choices[0].message.tool_calls[0]
    function_name = result.function.name                    # 获取函数名称
    function_args = result.function.arguments               # 获取函数参数
    function_id = result.id                                 # 获取函数调用ID
    model_info = response.choices[0].message.model_dump()   # 获取总的回复结果
    print("决策结果：", function_name, function_args, function_id, "\n\n")  # 打印决策结果
    messages.append(model_info)                             # 将决策结果添加到消息列表      

    # 三.执行：根据决策结果，执行对应的工具。
    if function_name == "write_txt":                        # 如果是写入文本的工具
        result = write_txt(**json.loads(function_args))     # 执行写入文本的工具
    if function_name == "screen_shot":                      # 如果是截图的工具
        result = screen_shot(**json.loads(function_args))   # 执行截图的工具
    if function_name == "weather_index":                    # 如果是天气查询的工具
        result = weather_index(**json.loads(function_args)) # 执行天气查询的工具
    print("工具执行结果：", result, "\n\n")                  # 打印工具执行结果
    message = {"role" : "tool", 
               "name" : function_name, 
               "content" : str(result),                     # 大模型接收的工具执行结果必须是字符串。
               "tool_call_id": function_id}                 # 构建工具执行结果消息
    messages.append(message)                                # 将工具执行结果添加到消息列表

    # 四.观察：将执行结果反馈给大模型
    response = client.chat.completions.create(
        model = model_name,                               # 模型名称      
        messages = messages,                              # 消息列表
    )
    result = response.choices[0].message.content          # 获取模型的回复内容
    print("第二次回复：", result, "\n\n")                  # 打印模型的
    message = {"role": "assistant", "content": result}    # 构建模型回复消息
    messages.append(message)                              # 将模型回复添加到消息列表



    