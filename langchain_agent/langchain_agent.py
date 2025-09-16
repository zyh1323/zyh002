from langchain_tools import ask_fruit_price, calculate, code_generate, write_code, code_execute
from langchain_openai.chat_models.base import BaseChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


# 一：创建聊天功能
llm = BaseChatOpenAI(
    model_name = "deepseek-chat",
    openai_api_key = "sk-9cc79d17dec3438e92ef90db423e20c1",
    openai_api_base = "https://api.deepseek.com")                  # 通过langchain的库，建立api调用的连接

# 二：创建agent
tools_list = [ask_fruit_price, calculate, code_generate, write_code, code_execute]
agent = create_react_agent(model = llm,
                           tools= tools_list)               # 通过langgraph的库，创建一个带有CoT的agent，把llm和工具传入

# 三：构建用户的输入
query = "请生成一段python代码，使用opencv绘制一个生动的小老虎，眼睛鼻子嘴巴。并保存和执行这段代码。"    # 用户输入
message = {"role": "user", "content": query}                        # 构建消息
messages = {"messages": [message]}                                  # 构建消息列表  
result = agent.stream(messages,
                      stream_mode = "values")                       # 让agent流式推理消息

# 四：打印输出结果
for i, step in enumerate(result):
    print("==========第{}步=========".format(i+1))                   # 打印步骤
    print(step["messages"][-1].content)                              # 打印输出