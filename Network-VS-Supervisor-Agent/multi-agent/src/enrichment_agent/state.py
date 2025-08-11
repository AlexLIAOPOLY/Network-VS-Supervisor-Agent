"""State definitions.

State is the interface between the graph and end user as well as the
data model used internally by the graph.
"""

from langgraph.graph import MessagesState

class AgentState(MessagesState):
    next: str