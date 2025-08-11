# Network vs Supervisor Multi-Agent Architecture

一个基于 LangGraph 的多智能体架构系统，实现了网络型和监督型两种不同的协作模式。

## 🌟 系统特点

### 三层分层架构
- **顶层监督者**：全局任务分析和团队协调
- **团队监督者**：专业领域团队管理  
- **专业代理**：具体任务执行

### 三个专业团队
- **研究团队**：文献研究、信息搜索、数据收集
- **分析团队**：数据分析、计算处理、可视化展示
- **执行团队**：代码编写、系统测试、部署运维

## 🚀 快速开始

### 环境准备

```bash
# 克隆项目
git clone https://github.com/AlexLIAOPOLY/Network-VS-Supervisor-Agent.git
cd Network-VS-Supervisor-Agent/multi-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -e .
```

### 配置环境变量

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 启动开发服务

```bash
# 启动 LangGraph 开发服务器
langgraph dev
```

访问 `http://localhost:8123` 查看 LangGraph Studio 界面

## 📊 架构设计

### 分层多智能体架构

```
顶层监督者
├── 研究团队监督者
│   ├── 研究员 (理论分析)
│   ├── 搜索员 (信息检索)
│   └── 数据收集员 (数据整理)
├── 分析团队监督者  
│   ├── 分析员 (数据分析)
│   ├── 计算员 (数值计算)
│   └── 图表员 (数据可视化)
└── 执行团队监督者
    ├── 代码员 (程序开发)
    ├── 测试员 (质量保证)
    └── 部署员 (系统运维)
```

### 网络型架构

```
用户输入 → 路由器 → 协调员 ← → 各专业代理 → 输出
```

## 🛠️ 核心组件

### 智能体类型

| 智能体 | 功能描述 | 工具集成 |
|--------|----------|----------|
| 研究员 | 理论分析、学术研究 | 文本分析 |
| 搜索员 | 网络搜索、信息收集 | Web搜索API |
| 分析员 | 数据分析、模式识别 | 统计工具 |
| 计算员 | 数学计算、统计分析 | Python REPL |
| 代码员 | 程序开发、代码实现 | 编程环境 |
| 图表员 | 数据可视化、图表制作 | Matplotlib |

### 工具集成

- **Python REPL**：代码执行和计算
- **Web搜索**：实时信息获取
- **数据处理**：统计分析和可视化

## 🔧 使用方法

### 1. 分层架构使用

```python
from enrichment_agent.hierarchical_graph import hierarchical_graph
from enrichment_agent.state import AgentState
from langchain_core.messages import HumanMessage

# 创建输入状态
state = AgentState(messages=[HumanMessage(content="分析股市趋势")])

# 执行任务
result = hierarchical_graph.invoke(state)
print(result["messages"][-1].content)
```

### 2. 网络架构使用

```python
from enrichment_agent.network_graph import network_graph
from enrichment_agent.state import AgentState

# 创建输入
state = AgentState(messages=[HumanMessage(content="开发一个Web应用")])

# 执行任务
result = network_graph.invoke(state)
```

## 🌐 部署选项

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 本地开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
ruff format .

# 类型检查
mypy .
```

## 📝 API文档

### 状态定义

```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    next: Optional[str]
```

### 主要接口

- `hierarchical_graph.invoke(state)` - 执行分层架构任务
- `network_graph.invoke(state)` - 执行网络架构任务
- `unified_graph.invoke(state)` - 执行统一架构任务

## 🔍 性能特点

- **模块化设计**：独立的团队和代理，易于维护
- **并行处理**：多个代理可同时工作
- **智能路由**：根据任务特点自动选择最佳代理
- **可扩展性**：支持添加新的团队和代理类型

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙋‍♂️ 支持

如有问题或建议，请创建 Issue 或联系项目维护者。

---

**注意**：确保正确配置环境变量，特别是 API 密钥，以确保系统正常运行。
