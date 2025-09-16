import pyautogui
import time
from openai import OpenAI
import json
import requests


# 准备工具和说明文档
# 截图工具，截取当前屏幕，并保存到指定路径。
def screen_shot(save_path):
    try:
        screenshot = pyautogui.screenshot()  # 截取当前屏幕
        screenshot.save(save_path)           # 保存截图到指定路径
        return "工具调用成功，截图已保存到：" + save_path
    except Exception as e:
        return "工具调用失败，错误信息：" + str(e)

# 将文本文件，并保存
def write_txt(text):
    try:
        time_current = str(int(time.time()))          # 获取当前时间戳
        file_name = "../data/txt/" + time_current + ".txt"  # 构建文件名
        with open(file_name, "w", encoding="utf-8") as f:  # 打开文件
            f.write(text)                               # 写入文本
        return "工具调用成功，文本已写入并保存。"
    except Exception as e:
        return "工具调用失败，错误信息：" + str(e)

# 天气查询工具
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


# 定义工具列表
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
         "description": "将文本写入文件，并保存",                 # 工具的描述
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
                     "description": "城市编号"         # 参数一的描述
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
model_name = "deepseek-reasoner"                      # DeepSeek的模型名称
client = OpenAI(api_key=api_key, base_url=url)    # 简历连接
messages = []                                     # 消息列表

# 准备提示词模版
prompt = """
# 一：你是一个智能体，你可以根据工具列表和用户需求做出决策。

# 二：你的任务是根据用户的输入以及工具列表，决定要调用哪个工具，并且从用户需求中抽取出相应的参数。

# 三：你必须严格按照我给定的示例模版进行输出，不要输出其他无关内容，比如```json```。
{{
"function_name": "weather_index",
"function_args": {{"city": "140100"}}
}}
如果不需要调用任何工具，则输出：
None

# 四：工具列表如下：
{tools_list}

# 五：用户的输入如下：

""".format(tools_list=str(tools_list))



# 一.感知： LLM接收用户的输入
query = "请帮我查询山西太原的天气，城市编号：140100"                        # 用户输入的内容
message = {"role": "user", "content": prompt + query}      # 构建消息
messages.append(message)                          # 将用户输入添加到消息列表
response = client.chat.completions.create(
    model = model_name,                           # 模型名称      
    messages = messages,                          # 消息列表
)
print("\n第一次回复：", response, "\n\n")          # 打印模型的回复


# 二.规划：决定要调用哪一个函数，以及函数的参数。
if response.choices[0].message.content:                  # 如果需要调用工具，执行下面的流程
    result = response.choices[0].message.content         # 获取大模型的返回结果
    result = json.loads(result)
    function_name = result["function_name"]                  # 获取函数名称
    function_args = result["function_args"]                   # 获取函数参数
    print("决策结果：", function_name, function_args, "\n\n")  # 打印决策结果

    # 三.执行：根据决策结果，执行对应的工具。
    if function_name == "write_txt":                        # 如果是写入文本的工具
        result = write_txt(**function_args)                 # 执行写入文本的工具
    if function_name == "screen_shot":                      # 如果是截图的工具
        result = screen_shot(**function_args)               # 执行截图的工具
    if function_name == "weather_index":                    # 如果是天气查询的工具
        result = weather_index(**function_args)             # 执行天气查询的工具
    print("工具执行结果：", result, "\n\n")                  # 打印工具执行结果

    # 四. 观察：将执行结果反馈给大模型
    prompt_new = """
                你的任务是根据用户的输入以及工具的执行结果给出最终的回复。
                用户的输入是：{query}
                工具的执行结果是：{result}
                """.format(query=query, result=result)   # 构建新的提示词
    message = {"role": "user", "content": prompt_new}    # 构建新的用户消息
    messages = []                               # 清空消息列表
    messages.append(message)                    # 将新的用户消息添加到消息列表
    response = client.chat.completions.create(
        model = model_name,                               # 模型名称      
        messages = messages,                              # 消息列表
    )
    result = response.choices[0].message.content          # 获取模型的回复内容
    print("第二次回复：", result, "\n\n")                  # 打印模型