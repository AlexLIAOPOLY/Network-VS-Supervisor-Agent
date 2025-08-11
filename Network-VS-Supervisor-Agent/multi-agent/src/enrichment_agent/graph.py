"""Define a data enrichment agent.

Works with a chat model with tool calling support.
"""

import os
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from enrichment_agent.tools import python_repl, web_search  # , add_sale, delete_sale, update_sale, query_sales  # SQL工具暂时注释
from enrichment_agent.state import AgentState
# TypedDict 和 Literal 导入已移除，不再需要结构化输出


# 用于普通问答对话
chat_llm = ChatOpenAI(model="deepseek-chat",
                   api_key=os.getenv('DEEPSEEK_API_KEY'),
                   base_url='https://api.deepseek.com')

# 用于数据库检索
db_llm = ChatOpenAI(model="deepseek-chat",
                   api_key=os.getenv('DEEPSEEK_API_KEY'),
                   base_url='https://api.deepseek.com')

# 用于代码生成和执行代码
coder_llm = ChatOpenAI(model="deepseek-chat",
                   api_key=os.getenv('DEEPSEEK_API_KEY'),
                   base_url='https://api.deepseek.com')


# 创建 模型
# db_agent = create_react_agent(
#     db_llm,
#     tools=[add_sale, delete_sale, update_sale, query_sales],
#     state_modifier="You use to perform database operations while should provide accurate data for the code_generator to use"
# )

search_agent = create_react_agent(
    chat_llm,
    tools=[web_search]
)

code_agent = create_react_agent(
    coder_llm,
    tools=[python_repl]
)

# 创建普通对话问答节点
def chat(state: AgentState):
    messages = state["messages"]
    model_response = chat_llm.invoke(messages)
    final_response = [AIMessage(content=model_response.content, name="chatbot")]
    return {"messages": final_response}

# 创建执行数据库操作节点（暂时注释）
# def db_node(state: AgentState):
#     result = db_agent.invoke(state)
#     return {
#         "messages": [
#             HumanMessage(content=result["messages"][-1].content, name="sqler")
#         ]
#     }

# 创建信息检索节点
def search_node(state: AgentState):
    result = search_agent.invoke(state)
    return {
        "messages": [
            AIMessage(content=result["messages"][-1].content, name="searcher")
        ]
    }

# 创建代码执行节点
def code_node(state: AgentState):
    result = code_agent.invoke(state)
    return {
        "messages": [AIMessage(content=result["messages"][-1].content, name="coder")]
    }


# 任何一个代理都可以决定结束

members = ["chat", "coder", "searcher"]  # 替换sqler为searcher
options = members + ["FINISH"]


# Router类已移除，改用文本输出方式


def supervisor(state: AgentState):
    messages = state["messages"]
    
    # 如果没有消息，开始对话
    if not messages:
        return {"next": "chat"}
    
    # 获取最后一条消息
    last_message = messages[-1]
    
    # 如果最后一条消息是AI回复，检查是否需要继续对话
    if hasattr(last_message, 'name') and last_message.name in ['chatbot', 'searcher', 'coder']:
        # 检查对话是否已经完成
        # 如果用户的问题已经得到回答，结束对话
        system_prompt = (
            "You are a supervisor. Review the conversation and determine if the user's question has been adequately answered.\n"
            "If the answer is complete and satisfactory, respond with 'FINISH'.\n"
            "If more information is needed, choose the most appropriate worker:\n"
            "- chat: For general conversation and questions\n"
            "- coder: For code execution, data analysis, or creating visualizations\n"  
            "- searcher: For searching current information on the internet\n"
            f"Available options: {', '.join(options)}\n"
            "Respond with only one word: the worker name or FINISH."
        )
        
        # 构建消息历史给LLM分析
        conversation_summary = []
        for msg in messages[-3:]:  # 只看最近3条消息
            role = "user" if not hasattr(msg, 'name') else "assistant"
            conversation_summary.append({"role": role, "content": str(msg.content)})
        
        analysis_messages = [{"role": "system", "content": system_prompt}] + conversation_summary
        
        response = db_llm.invoke(analysis_messages)
        next_ = response.content.strip().upper()
        
        if next_ in ["CHAT", "CODER", "SEARCHER"]:
            next_ = next_.lower()
        elif next_ == "FINISH":
            next_ = END
        else:
            # 如果回答已经完整，结束对话
            next_ = END
    else:
        # 如果是用户消息，使用LLM来选择合适的worker
        user_message = str(last_message.content)
        
        system_prompt = (
            "You are a task router. Based on the user's request, choose the most appropriate worker:\n"
            "- searcher: For internet searches, finding current information, news, weather, or any request that needs web search\n"
            "- coder: For programming, data analysis, calculations, creating charts/plots, or any code execution\n"
            "- chat: For general conversation, questions that can be answered with existing knowledge\n"
            f"Available options: {', '.join(members)}\n"
            "Respond with only one word: searcher, coder, or chat"
        )
        
        router_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User request: {user_message}"}
        ]
        response = db_llm.invoke(router_messages)
        next_ = response.content.strip().lower()
        
        # 添加调试日志
        print(f"DEBUG: User message: {user_message}")
        print(f"DEBUG: LLM选择的agent: {next_}")
        
        # 验证返回的选择是否有效
        if next_ not in members:
            print(f"DEBUG: LLM返回无效选择 '{next_}', 使用备用关键词匹配")
            # 备用关键词匹配
            if any(keyword in user_message.lower() for keyword in ['搜索', '查找', '上网', '网上', '搜', '最新', '新闻', 'search', 'find', 'latest', 'news', 'google', '百度']):
                next_ = "searcher"
                print(f"DEBUG: 关键词匹配选择 searcher")
            elif any(keyword in user_message.lower() for keyword in ['代码', '编程', '计算', '图表', '数据', '画图', 'code', 'python', 'chart', 'plot', 'calculate', 'draw']):
                next_ = "coder" 
                print(f"DEBUG: 关键词匹配选择 coder")
            else:
                next_ = "chat"
                print(f"DEBUG: 默认选择 chat")
        else:
            print(f"DEBUG: LLM有效选择: {next_}")
    
    return {"next": next_}


workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("chat", chat)
workflow.add_node("coder", code_node)
workflow.add_node("searcher", search_node)  # 替换sqler为searcher
# workflow.add_node("sqler", db_node)  # 暂时注释数据库节点

for member in members:
    # 每个子代理在完成工作后总是向主管“汇报”
    workflow.add_edge(member, "supervisor")

workflow.add_edge(START, "supervisor")
# 在图状态中填充`next`字段，路由到具体的某个节点或者结束图的运行，从来指定如何执行接下来的任务。
workflow.add_conditional_edges(
    "supervisor", 
    lambda state: state["next"],
    {member: member for member in members} | {END: END}
)

# 编译图
graph = workflow.compile()

graph.name = "multi-Agent"

