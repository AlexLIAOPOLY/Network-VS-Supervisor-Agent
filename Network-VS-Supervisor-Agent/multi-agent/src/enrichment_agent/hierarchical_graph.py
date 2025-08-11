"""分层多代理架构 (Hierarchical Multi-Agent Architecture)

这个模块实现了三层架构：
1. 顶层监督者 - 协调各个团队
2. 团队监督者 - 管理团队内的专业代理
3. 专业代理 - 执行具体任务

架构特点：
- 模块化：每个团队负责特定领域
- 层次化：清晰的管理层级
- 专业化：每个代理都有专门技能
- 可扩展：容易添加新的团队和代理
"""

import os
from typing import Literal, List, Dict, Any
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from enrichment_agent.tools import python_repl, web_search
from enrichment_agent.state import AgentState


# 创建LLM实例
hierarchical_llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url='https://api.deepseek.com'
)

# ============================================================================
# 第三层：专业代理（底层执行者）
# ============================================================================

def researcher_agent(state: AgentState):
    """研究员代理 - 负责文献研究和理论分析"""
    messages = state["messages"]
    
    # 专业研究提示
    research_prompt = """
    你是一个专业的研究员。你的任务是：
    1. 进行深入的理论分析
    2. 查找相关文献和资料
    3. 提供学术观点和见解
    
    请基于用户的需求进行专业的研究分析。
    """
    
    enhanced_messages = [{"role": "system", "content": research_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    response = hierarchical_llm.invoke(enhanced_messages)
    return {"messages": [AIMessage(content=response.content, name="researcher")]}


def searcher_agent(state: AgentState):
    """搜索员代理 - 使用搜索工具获取最新信息"""
    search_agent = create_react_agent(hierarchical_llm, tools=[web_search])
    result = search_agent.invoke(state)
    return {"messages": [AIMessage(content=result["messages"][-1].content, name="searcher")]}


def data_collector_agent(state: AgentState):
    """数据收集员代理 - 负责数据收集和整理"""
    messages = state["messages"]
    
    data_prompt = """
    你是一个数据收集专家。你的任务是：
    1. 识别需要收集的数据类型
    2. 制定数据收集计划
    3. 整理和清洗数据
    
    请根据用户需求制定数据收集方案。
    """
    
    enhanced_messages = [{"role": "system", "content": data_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    response = hierarchical_llm.invoke(enhanced_messages)
    return {"messages": [AIMessage(content=response.content, name="data_collector")]}


def analyst_agent(state: AgentState):
    """分析员代理 - 进行数据分析和解释"""
    messages = state["messages"]
    
    analysis_prompt = """
    你是一个专业分析师。你的任务是：
    1. 分析数据中的模式和趋势
    2. 提供深入的洞察和解释
    3. 识别关键发现和异常
    
    请对提供的信息进行专业分析。
    """
    
    enhanced_messages = [{"role": "system", "content": analysis_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    response = hierarchical_llm.invoke(enhanced_messages)
    return {"messages": [AIMessage(content=response.content, name="analyst")]}


def calculator_agent(state: AgentState):
    """计算员代理 - 使用代码进行计算"""
    calc_agent = create_react_agent(hierarchical_llm, tools=[python_repl])
    result = calc_agent.invoke(state)
    return {"messages": [AIMessage(content=result["messages"][-1].content, name="calculator")]}


def visualizer_agent(state: AgentState):
    """图表员代理 - 创建可视化图表"""
    messages = state["messages"]
    
    viz_prompt = """
    你是一个可视化专家。你的任务是：
    1. 设计合适的图表类型
    2. 创建清晰的数据可视化
    3. 提供图表解释说明
    
    请根据数据特点设计最佳的可视化方案。
    """
    
    enhanced_messages = [{"role": "system", "content": viz_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    response = hierarchical_llm.invoke(enhanced_messages)
    return {"messages": [AIMessage(content=response.content, name="visualizer")]}


def coder_agent(state: AgentState):
    """代码员代理 - 编写和执行代码"""
    code_agent = create_react_agent(hierarchical_llm, tools=[python_repl])
    result = code_agent.invoke(state)
    return {"messages": [AIMessage(content=result["messages"][-1].content, name="coder")]}


def tester_agent(state: AgentState):
    """测试员代理 - 进行测试和验证"""
    messages = state["messages"]
    
    test_prompt = """
    你是一个专业测试工程师。你的任务是：
    1. 设计测试方案和测试用例
    2. 执行功能测试和性能测试
    3. 识别问题和提供改进建议
    
    请制定全面的测试计划。
    """
    
    enhanced_messages = [{"role": "system", "content": test_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    response = hierarchical_llm.invoke(enhanced_messages)
    return {"messages": [AIMessage(content=response.content, name="tester")]}


def deployer_agent(state: AgentState):
    """部署员代理 - 负责部署和上线"""
    messages = state["messages"]
    
    deploy_prompt = """
    你是一个部署工程师。你的任务是：
    1. 制定部署计划和策略
    2. 配置生产环境
    3. 监控系统运行状态
    
    请提供详细的部署方案。
    """
    
    enhanced_messages = [{"role": "system", "content": deploy_prompt}] + [
        {"role": "user" if not hasattr(msg, 'name') else "assistant", 
         "content": str(msg.content)} for msg in messages
    ]
    
    response = hierarchical_llm.invoke(enhanced_messages)
    return {"messages": [AIMessage(content=response.content, name="deployer")]}


# ============================================================================
# 第二层：团队监督者（中层管理）
# ============================================================================

def research_team_supervisor(state: AgentState):
    """研究团队监督者 - 管理研究团队的工作分配"""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    # 如果来自顶层监督者的任务分配
    if hasattr(last_message, 'name') and last_message.name == "top_supervisor":
        task_content = str(last_message.content)
        
        # 分析任务类型，选择合适的研究团队成员
        decision_prompt = f"""
        作为研究团队的监督者，你需要分析以下任务并选择最合适的团队成员执行：

        任务内容：{task_content}

        可选的团队成员：
        - researcher: 擅长理论分析和学术研究
        - searcher: 擅长网络搜索和信息收集  
        - data_collector: 擅长数据收集和整理

        请选择一个最适合的成员，只回复成员名称：researcher, searcher, 或 data_collector
        """
        
        response = hierarchical_llm.invoke([{"role": "system", "content": decision_prompt}])
        choice = response.content.strip().lower()
        
        if choice not in ["researcher", "searcher", "data_collector"]:
            choice = "researcher"  # 默认选择
            
        return {
            "messages": [AIMessage(content=f"研究团队接收任务，分配给{choice}", name="research_supervisor")],
            "next": choice
        }
    else:
        # 来自团队成员的报告，决定是否需要其他成员协助或完成任务
        return {
            "messages": [AIMessage(content="研究团队任务完成", name="research_supervisor")],
            "next": "FINISH"
        }


def analysis_team_supervisor(state: AgentState):
    """分析团队监督者 - 管理分析团队的工作分配"""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    if hasattr(last_message, 'name') and last_message.name == "top_supervisor":
        task_content = str(last_message.content)
        
        decision_prompt = f"""
        作为分析团队的监督者，你需要分析以下任务并选择最合适的团队成员执行：

        任务内容：{task_content}

        可选的团队成员：
        - analyst: 擅长数据分析和模式识别
        - calculator: 擅长数学计算和统计分析
        - visualizer: 擅长数据可视化和图表制作

        请选择一个最适合的成员，只回复成员名称：analyst, calculator, 或 visualizer
        """
        
        response = hierarchical_llm.invoke([{"role": "system", "content": decision_prompt}])
        choice = response.content.strip().lower()
        
        if choice not in ["analyst", "calculator", "visualizer"]:
            choice = "analyst"
            
        return {
            "messages": [AIMessage(content=f"分析团队接收任务，分配给{choice}", name="analysis_supervisor")],
            "next": choice
        }
    else:
        return {
            "messages": [AIMessage(content="分析团队任务完成", name="analysis_supervisor")],
            "next": "FINISH"
        }


def execution_team_supervisor(state: AgentState):
    """执行团队监督者 - 管理执行团队的工作分配"""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    if hasattr(last_message, 'name') and last_message.name == "top_supervisor":
        task_content = str(last_message.content)
        
        decision_prompt = f"""
        作为执行团队的监督者，你需要分析以下任务并选择最合适的团队成员执行：

        任务内容：{task_content}

        可选的团队成员：
        - coder: 擅长编程和代码实现
        - tester: 擅长测试和质量保证
        - deployer: 擅长部署和运维

        请选择一个最适合的成员，只回复成员名称：coder, tester, 或 deployer
        """
        
        response = hierarchical_llm.invoke([{"role": "system", "content": decision_prompt}])
        choice = response.content.strip().lower()
        
        if choice not in ["coder", "tester", "deployer"]:
            choice = "coder"
            
        return {
            "messages": [AIMessage(content=f"执行团队接收任务，分配给{choice}", name="execution_supervisor")],
            "next": choice
        }
    else:
        return {
            "messages": [AIMessage(content="执行团队任务完成", name="execution_supervisor")],
            "next": "FINISH"
        }


# ============================================================================
# 第一层：顶层监督者（最高层决策）
# ============================================================================

def top_level_supervisor(state: AgentState):
    """顶层监督者 - 分析任务并分配给合适的团队"""
    messages = state["messages"]
    user_input = str(messages[-1].content) if messages else ""
    
    # 分析用户请求，决定分配给哪个团队
    decision_prompt = f"""
    作为顶层监督者，你需要分析用户的请求并决定分配给哪个专业团队：

    用户请求：{user_input}

    可选的团队：
    - research_team: 适合理论研究、文献调查、概念分析等任务
    - analysis_team: 适合数据分析、统计计算、可视化等任务  
    - execution_team: 适合编程实现、测试部署、系统开发等任务

    请分析任务特点并选择最适合的团队，只回复团队名称：research_team, analysis_team, 或 execution_team
    """
    
    response = hierarchical_llm.invoke([{"role": "system", "content": decision_prompt}])
    team_choice = response.content.strip().lower()
    
    # 验证选择的有效性
    valid_teams = ["research_team", "analysis_team", "execution_team"]
    if team_choice not in valid_teams:
        team_choice = "research_team"  # 默认选择研究团队
    
    # 生成任务分配消息
    task_message = f"顶层监督者分析用户需求：{user_input}，决定分配给{team_choice}团队处理"
    
    return {
        "messages": [AIMessage(content=task_message, name="top_supervisor")],
        "next": team_choice
    }


# ============================================================================
# 路由器函数
# ============================================================================

def hierarchical_router(state: AgentState):
    """分层路由器 - 根据状态决定下一个节点"""
    next_node = state.get("next", "research_team")
    
    if next_node == "FINISH":
        return END
    
    return next_node


# ============================================================================
# 构建分层多代理图
# ============================================================================

# 创建状态图
hierarchical_workflow = StateGraph(AgentState)

# 添加顶层监督者
hierarchical_workflow.add_node("top_supervisor", top_level_supervisor)

# 添加团队监督者（第二层）
hierarchical_workflow.add_node("research_team", research_team_supervisor)
hierarchical_workflow.add_node("analysis_team", analysis_team_supervisor) 
hierarchical_workflow.add_node("execution_team", execution_team_supervisor)

# 添加专业代理（第三层）
# 研究团队成员
hierarchical_workflow.add_node("researcher", researcher_agent)
hierarchical_workflow.add_node("searcher", searcher_agent)
hierarchical_workflow.add_node("data_collector", data_collector_agent)

# 分析团队成员
hierarchical_workflow.add_node("analyst", analyst_agent)
hierarchical_workflow.add_node("calculator", calculator_agent)
hierarchical_workflow.add_node("visualizer", visualizer_agent)

# 执行团队成员
hierarchical_workflow.add_node("coder", coder_agent)
hierarchical_workflow.add_node("tester", tester_agent)
hierarchical_workflow.add_node("deployer", deployer_agent)

# ============================================================================
# 添加边和路由逻辑
# ============================================================================

# 从开始节点到顶层监督者
hierarchical_workflow.add_edge(START, "top_supervisor")

# 初始的顶层监督者到团队监督者的条件边（仅用于首次任务分配）
def initial_router(state: AgentState):
    """初始路由器 - 仅用于首次从顶层监督者分配任务"""
    next_node = state.get("next", "research_team")
    if next_node == "FINISH":
        return END
    return next_node


# 专业代理完成后向上报告给团队监督者（实现向上通信）
# 研究团队成员向研究团队监督者报告
hierarchical_workflow.add_edge("researcher", "research_team")
hierarchical_workflow.add_edge("searcher", "research_team") 
hierarchical_workflow.add_edge("data_collector", "research_team")

# 分析团队成员向分析团队监督者报告
hierarchical_workflow.add_edge("analyst", "analysis_team")
hierarchical_workflow.add_edge("calculator", "analysis_team")
hierarchical_workflow.add_edge("visualizer", "analysis_team")

# 执行团队成员向执行团队监督者报告
hierarchical_workflow.add_edge("coder", "execution_team")
hierarchical_workflow.add_edge("tester", "execution_team") 
hierarchical_workflow.add_edge("deployer", "execution_team")

# 团队监督者完成后决定下一步（向上报告或继续分配任务）
def team_supervisor_router(state: AgentState):
    """团队监督者路由器 - 处理向上报告或继续分配任务"""
    next_node = state.get("next", "FINISH")
    
    # 如果任务完成，向上报告给顶层监督者
    if next_node == "FINISH":
        return "top_supervisor"
    
    # 否则继续分配给专业代理
    return next_node

# 顶层监督者最终路由器 - 决定是否结束整个流程
def top_supervisor_final_router(state: AgentState):
    """顶层监督者最终路由器 - 决定是否结束整个流程"""
    messages = state.get("messages", [])
    
    # 检查是否有团队监督者的报告
    supervisor_reports = [msg for msg in messages if hasattr(msg, 'name') and 
                         msg.name in ["research_supervisor", "analysis_supervisor", "execution_supervisor"]]
    
    # 如果已有报告，结束流程
    if supervisor_reports:
        return END
    
    # 否则继续分配任务（初次分配）
    next_node = state.get("next", "research_team")
    return next_node

# 首次任务分配和后续向上报告的条件边
hierarchical_workflow.add_conditional_edges(
    "top_supervisor",
    top_supervisor_final_router,
    {
        "research_team": "research_team",
        "analysis_team": "analysis_team",
        "execution_team": "execution_team",
        END: END
    }
)

# 更新团队监督者的条件边，支持向上通信和向下分配
hierarchical_workflow.add_conditional_edges(
    "research_team",
    team_supervisor_router,
    {
        "researcher": "researcher",
        "searcher": "searcher", 
        "data_collector": "data_collector",
        "top_supervisor": "top_supervisor"
    }
)

hierarchical_workflow.add_conditional_edges(
    "analysis_team",
    team_supervisor_router,
    {
        "analyst": "analyst",
        "calculator": "calculator",
        "visualizer": "visualizer",
        "top_supervisor": "top_supervisor"
    }
)

hierarchical_workflow.add_conditional_edges(
    "execution_team", 
    team_supervisor_router,
    {
        "coder": "coder",
        "tester": "tester", 
        "deployer": "deployer",
        "top_supervisor": "top_supervisor"
    }
)


# 编译图
hierarchical_graph = hierarchical_workflow.compile()
hierarchical_graph.name = "Hierarchical-Multi-Agent"