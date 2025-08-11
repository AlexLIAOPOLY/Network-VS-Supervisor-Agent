"""统一的多代理图选择器.

这个模块允许用户选择使用 Supervisor 架构或 Network 架构。
"""

from enrichment_agent.graph import graph as supervisor_graph
from enrichment_agent.network_graph import network_graph


class GraphSelector:
    """图选择器类，用于选择不同的多代理架构"""
    
    def __init__(self):
        self.supervisor_graph = supervisor_graph
        self.network_graph = network_graph
    
    def get_supervisor_graph(self):
        """获取 Supervisor 架构的图"""
        return self.supervisor_graph
    
    def get_network_graph(self):
        """获取 Network 架构的图"""
        return self.network_graph
    
    def compare_architectures(self):
        """比较两种架构的特点"""
        comparison = {
            "Supervisor 架构": {
                "特点": [
                    "中央控制：有一个 supervisor 节点统一调度",
                    "层次化：明确的上下级关系",
                    "可预测：路由逻辑集中，容易理解和调试",
                    "适用场景：有明确工作流程的任务"
                ],
                "优势": ["控制精确", "逻辑清晰", "易于维护"],
                "劣势": ["中心化瓶颈", "灵活性较低"]
            },
            "Network 架构": {
                "特点": [
                    "去中心化：没有中央控制节点",
                    "自主决策：每个 agent 独立决定下一步",
                    "动态路由：agent 间可以自由通信",
                    "适用场景：复杂的、非线性的任务流程"
                ],
                "优势": ["高度灵活", "适应性强", "无单点故障"],
                "劣势": ["路由复杂", "可能出现死循环", "调试困难"]
            }
        }
        return comparison


# 创建全局选择器实例
graph_selector = GraphSelector()


def get_graph_by_type(graph_type="supervisor"):
    """根据类型获取相应的图
    
    Args:
        graph_type (str): "supervisor" 或 "network"
    
    Returns:
        相应的图对象
    """
    if graph_type.lower() == "network":
        return graph_selector.get_network_graph()
    else:
        return graph_selector.get_supervisor_graph()


def demo_both_graphs():
    """演示两种图的使用方法"""
    print("=== Supervisor 架构演示 ===")
    print("特点：中央 supervisor 节点统一调度")
    print("使用方法：")
    print("from enrichment_agent.unified_graph import get_graph_by_type")
    print("supervisor_graph = get_graph_by_type('supervisor')")
    print("result = supervisor_graph.invoke({'messages': [user_message]})")
    
    print("\n=== Network 架构演示 ===")
    print("特点：agent 之间自主决策，去中心化")
    print("使用方法：")
    print("from enrichment_agent.unified_graph import get_graph_by_type")
    print("network_graph = get_graph_by_type('network')")
    print("result = network_graph.invoke({'messages': [user_message]})")


if __name__ == "__main__":
    demo_both_graphs()
    print("\n=== 架构对比 ===")
    comparison = graph_selector.compare_architectures()
    for arch_name, details in comparison.items():
        print(f"\n{arch_name}:")
        for key, value in details.items():
            print(f"  {key}: {value}")