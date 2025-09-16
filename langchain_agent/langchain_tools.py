from langchain_core.tools import tool
from openai import OpenAI
import time
import os
import sys
import subprocess


@tool
def ask_fruit_price(fruit):
    """
    获取水果的价格
    : param fruit: 水果名称
    : return: 水果价格
    """
    if "苹果" in fruit or "apple" in fruit:
        return "苹果的价格是5元/公斤"
    elif "香蕉" in fruit or "banana" in fruit:
        return "香蕉的价格是3元/公斤"
    else:
        return "其他水果的价格为10元/公斤"

@tool
def calculate(expression):
    """
    运算计算函数进行计算并返回相应的结果。
    : param expression: 数学表达式
    : return: 计算结果
    """
    result = eval(expression)           # 计算字符串的表达式
    return result

@tool
def code_generate(requirement):
    """
    python代码生成工具，根据用户的需求生成相应的python代码
    : param requirement: 用户的需求
    : return: 生成的python代码
    """
    url = "https://api.deepseek.com"                  # DeepSeek的API地址
    api_key = "sk-9cc79d17dec3438e92ef90db423e20c1"   # DeepSeek的API密钥
    model_name = "deepseek-chat"                      # DeepSeek的模型名称
    client = OpenAI(api_key=api_key, base_url=url)    # 简历连接
    prompt = """
    # 一：你是一个资深的python开发工程师
    # 二：根据用户的需求，生成相应的python代码
    # 三：请不要生成任何多余的解释和描述，不要生成```python```，只需要生成代码即可。
    # 四：用户的需求如下：
    """
    query = prompt + requirement                       # 构建用户的输入
    message = {"role": "user", "content": query}    # 构建消息
    messages = [message]                                # 消息列表     
    response = client.chat.completions.create(         # 调用大模型
        model = model_name,                           # 模型名称      
        messages = messages                           # 消息列表
    )   
    result = response.choices[0].message.content      # 获取模型的回复
    return result

@tool
def write_code(code):
    """
    将代码写入文件中并保存
    : param code: 代码内容
    : return: 保存的文件的路径
    """
    save_path = "../data/code/"                        # 代码保存的路径
    time_current = str(int(time.time()))               # 获取当前的时间戳，并转为整数和字符串
    full_path = save_path + time_current + ".py"       # 拼接文件的完整路径
    if not os.path.exists(save_path):                   # 查看保存路径是否存在
        os.makedirs(save_path)                         # 如果不存在就创建这个文件
    with open(full_path, "w", encoding="utf-8") as f:  # 打开文件
        f.write(code)                                  # 将代码写入文件
    return full_path                                   # 返回文件的路径

@tool
def code_execute(file_path):
    """
    执行指定路径的python代码文件，并返回执行结果
    """
    try:
        cmd = [sys.executable, file_path]  # 构建命令列表
        process = subprocess.run(
            cmd,
            capture_output=True,  # 捕获标准输出和错误输出
        )
        return "代码执行完成。"
    except Exception as e:
        return "代码执行出错，错误信息：{}".format(str(e))


if __name__ == "__main__":
    pass