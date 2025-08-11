"""Network-based multi-agent architecture.

This implements a decentralized approach where agents can communicate 
directly with each other without a central supervisor.
"""

import os
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from enrichment_agent.tools import python_repl, web_search
from enrichment_agent.state import AgentState


# 创建模型实例
network_llm = ChatOpenAI(model="deepseek-chat",
                        api_key=os.getenv('DEEPSEEK_API_KEY'),
                        base_url='https://api.deepseek.com')

# 创建代理
network_search_agent = create_react_agent(
    network_llm,
    tools=[web_search]
)

network_code_agent = create_react_agent(
    network_llm,
    tools=[python_repl]
)


def network_chat_node(state: AgentState):
    """网络聊天节点 - 可以直接决定下一个节点"""
    messages = state["messages"]
    
    # 添加决策提示
    decision_prompt = """
    你是一个网络架构中的聊天代理。根据用户的请求，你需要：
    1. 回答用户的问题
    2. 决定是否需要调用其他代理协助
    
    如果需要其他代理协助：
    - 如果需要搜索信息，在回复末尾添加 [ROUTE:network_searcher]
    - 如果需要执行代码，在回复末尾添加 [ROUTE:network_coder]  
    - 如果任务完成，在回复末尾添加 [ROUTE:FINISH]
    """
    
    # 构建消息
    enhanced_messages = [{"role": "system", "content": decision_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    model_response = network_llm.invoke(enhanced_messages)
    response_content = model_response.content
    
    # 解析路由决策
    next_agent = "FINISH"
    if "[ROUTE:network_searcher]" in response_content:
        next_agent = "network_searcher"
        response_content = response_content.replace("[ROUTE:network_searcher]", "")
    elif "[ROUTE:network_coder]" in response_content:
        next_agent = "network_coder"
        response_content = response_content.replace("[ROUTE:network_coder]", "")
    elif "[ROUTE:FINISH]" in response_content:
        next_agent = "FINISH"
        response_content = response_content.replace("[ROUTE:FINISH]", "")
    
    final_response = [AIMessage(content=response_content.strip(), name="network_chatbot")]
    return {"messages": final_response, "next": next_agent}


def network_search_node(state: AgentState):
    """网络搜索节点 - 可以决定下一步行动"""
    result = network_search_agent.invoke(state)
    search_result = result["messages"][-1].content
    
    # 搜索后的决策逻辑
    decision_prompt = f"""
    你刚完成了一次搜索，结果是：{search_result}
    
    现在决定下一步：
    - 如果搜索结果需要进一步的代码分析或计算，在回复末尾添加 [ROUTE:network_coder]
    - 如果需要与用户进行更多交流，在回复末尾添加 [ROUTE:network_chat]
    - 如果任务已完成，在回复末尾添加 [ROUTE:FINISH]
    """
    
    decision_response = network_llm.invoke([{"role": "system", "content": decision_prompt}])
    decision_content = decision_response.content
    
    # 解析下一步
    next_agent = "FINISH"
    if "[ROUTE:network_coder]" in decision_content:
        next_agent = "network_coder"
    elif "[ROUTE:network_chat]" in decision_content:
        next_agent = "network_chat"
    elif "[ROUTE:FINISH]" in decision_content:
        next_agent = "FINISH"
    
    return {
        "messages": [AIMessage(content=search_result, name="network_searcher")],
        "next": next_agent
    }


def network_code_node(state: AgentState):
    """网络代码节点 - 可以决定下一步行动"""
    result = network_code_agent.invoke(state)
    code_result = result["messages"][-1].content
    
    # 代码执行后的决策逻辑
    decision_prompt = f"""
    你刚执行了代码，结果是：{code_result}
    
    现在决定下一步：
    - 如果需要搜索更多信息，在回复末尾添加 [ROUTE:network_searcher]
    - 如果需要与用户进行更多交流，在回复末尾添加 [ROUTE:network_chat]
    - 如果任务已完成，在回复末尾添加 [ROUTE:FINISH]
    """
    
    decision_response = network_llm.invoke([{"role": "system", "content": decision_prompt}])
    decision_content = decision_response.content
    
    # 解析下一步
    next_agent = "FINISH"
    if "[ROUTE:network_searcher]" in decision_content:
        next_agent = "network_searcher"
    elif "[ROUTE:network_chat]" in decision_content:
        next_agent = "network_chat"
    elif "[ROUTE:FINISH]" in decision_content:
        next_agent = "FINISH"
    
    return {
        "messages": [AIMessage(content=code_result, name="network_coder")],
        "next": next_agent
    }


def network_router(state: AgentState):
    """网络路由器 - 根据状态决定下一个节点"""
    next_node = state.get("next", "network_chat")
    
    if next_node == "FINISH":
        return END
    
    return next_node


# 构建网络图
network_workflow = StateGraph(AgentState)

# 添加节点
network_workflow.add_node("network_chat", network_chat_node)
network_workflow.add_node("network_searcher", network_search_node)
network_workflow.add_node("network_coder", network_code_node)

# 添加边 - 每个节点都可以路由到任何其他节点
network_workflow.add_edge(START, "network_chat")

# 添加条件边，每个节点都可以决定下一个节点
network_workflow.add_conditional_edges(
    "network_chat",
    network_router,
    {
        "network_searcher": "network_searcher",
        "network_coder": "network_coder",
        "network_chat": "network_chat",
        END: END
    }
)

network_workflow.add_conditional_edges(
    "network_searcher",
    network_router,
    {
        "network_chat": "network_chat",
        "network_coder": "network_coder",
        "network_searcher": "network_searcher",
        END: END
    }
)

network_workflow.add_conditional_edges(
    "network_coder",
    network_router,
    {
        "network_chat": "network_chat",
        "network_searcher": "network_searcher", 
        "network_coder": "network_coder",
        END: END
    }
)

# 编译网络图
network_graph = network_workflow.compile()
network_graph.name = "Network-Agent"