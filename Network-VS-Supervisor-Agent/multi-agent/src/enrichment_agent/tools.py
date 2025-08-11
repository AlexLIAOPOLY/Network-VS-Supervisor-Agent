"""Tools for data enrichment.

This module contains functions that are directly exposed to the LLM as tools.
These tools can be used for tasks such as web searching and scraping.
Users can edit and extend these tools as needed.
"""

import os
from typing_extensions import Annotated
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from langchain_experimental.utilities import PythonREPL
from pydantic import BaseModel
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建基类（暂时注释，避免数据库连接问题）
# Base = declarative_base()
# DATABASE_URI = 'mysql+pymysql://root:snowball2019@localhost/langgraph_agent?charset=utf8mb4'  # 这里要替换成自己的数据库连接串
# # DATABASE_URI = 'mysql+pymysql://root:snowball2019@langgraph-mysql/langgraph_agent?charset=utf8mb4'
# engine = create_engine(DATABASE_URI)
# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

repl = PythonREPL()

# 创建TAVILY搜索工具
tavily_search = TavilySearchResults(
    max_results=5,
    api_key=os.getenv('TAVILY_API_KEY')
)

# 信息检索工具
@tool
def web_search(
    query: Annotated[str, "搜索查询关键词，用于在网络上搜索最新信息"]
):
    """使用Tavily搜索引擎在互联网上搜索信息，获取最新、准确的结果。"""
    try:
        results = tavily_search.run(query)
        return f"搜索查询: {query}\n搜索结果:\n{results}"
    except Exception as e:
        return f"搜索失败，错误原因：{repr(e)}"


# 用于数据分析师执行代码
@tool
def python_repl(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str


# 定义模型（暂时注释，避免数据库连接问题）
# class SalesData(Base):
#     __tablename__ = 'sales_data'
#     sales_id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey('product_information.product_id'))
#     employee_id = Column(Integer)  # 示例简化，未创建员工表
#     customer_id = Column(Integer, ForeignKey('customer_information.customer_id'))
#     sale_date = Column(String(50))
#     quantity = Column(Integer)
#     amount = Column(Float)
#     discount = Column(Float)


# class CustomerInformation(Base):
#     __tablename__ = 'customer_information'
#     customer_id = Column(Integer, primary_key=True)
#     customer_name = Column(String(50))
#     contact_info = Column(String(50))
#     region = Column(String(50))
#     customer_type = Column(String(50))


# class ProductInformation(Base):
#     __tablename__ = 'product_information'
#     product_id = Column(Integer, primary_key=True)
#     product_name = Column(String(50))
#     category = Column(String(50))
#     unit_price = Column(Float)
#     stock_level = Column(Integer)


# class CompetitorAnalysis(Base):
#     __tablename__ = 'competitor_analysis'
#     competitor_id = Column(Integer, primary_key=True)
#     competitor_name = Column(String(50))
#     region = Column(String(50))
#     market_share = Column(Float)


# 数据库Schema（暂时注释，避免数据库连接问题）
# class AddSaleSchema(BaseModel):
#     product_id: int
#     employee_id: int
#     customer_id: int
#     sale_date: str
#     quantity: int
#     amount: float
#     discount: float


# class DeleteSaleSchema(BaseModel):
#     sales_id: int


# class UpdateSaleSchema(BaseModel):
#     sales_id: int
#     quantity: int
#     amount: float


# class QuerySalesSchema(BaseModel):
#     sales_id: int


# 重复的数据库定义（暂时注释，避免数据库连接问题）
# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import declarative_base

# # 创建基类
# Base = declarative_base()


# # 定义模型
# class SalesData(Base):
#     __tablename__ = 'sales_data'
#     sales_id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey('product_information.product_id'))
#     employee_id = Column(Integer)  # 示例简化，未创建员工表
#     customer_id = Column(Integer, ForeignKey('customer_information.customer_id'))
#     sale_date = Column(String(50))
#     quantity = Column(Integer)
#     amount = Column(Float)
#     discount = Column(Float)


# 1. 添加销售数据：（暂时注释，避免数据库连接问题）
# @tool(args_schema=AddSaleSchema)
# def add_sale(product_id, employee_id, customer_id, sale_date, quantity, amount, discount):
#     """Add sale record to the database."""
#     session = Session()
#     try:
#         new_sale = SalesData(
#             product_id=product_id,
#             employee_id=employee_id,
#             customer_id=customer_id,
#             sale_date=sale_date,
#             quantity=quantity,
#             amount=amount,
#             discount=discount
#         )
#         session.add(new_sale)
#         session.commit()
#         return {"messages": ["销售记录添加成功。"]}
#     except Exception as e:
#         return {"messages": [f"添加失败，错误原因：{e}"]}
#     finally:
#         session.close()


# 2. 删除销售数据（暂时注释，避免数据库连接问题）
# @tool(args_schema=DeleteSaleSchema)
# def delete_sale(sales_id):
#     """Delete sale record from the database."""
#     session = Session()
#     try:
#         sale_to_delete = session.query(SalesData).filter(SalesData.sales_id == sales_id).first()
#         if sale_to_delete:
#             session.delete(sale_to_delete)
#             session.commit()
#             return {"messages": ["销售记录删除成功。"]}
#         else:
#             return {"messages": [f"未找到销售记录ID：{sales_id}"]}
#     except Exception as e:
#         return {"messages": [f"删除失败，错误原因：{e}"]}
#     finally:
#         session.close()


# # 3. 修改销售数据（暂时注释，避免数据库连接问题）
# @tool(args_schema=UpdateSaleSchema)
# def update_sale(sales_id, quantity, amount):
#     """Update sale record in the database."""
#     session = Session()
#     try:
#         sale_to_update = session.query(SalesData).filter(SalesData.sales_id == sales_id).first()
#         if sale_to_update:
#             sale_to_update.quantity = quantity
#             sale_to_update.amount = amount
#             session.commit()
#             return {"messages": ["销售记录更新成功。"]}
#         else:
#             return {"messages": [f"未找到销售记录ID：{sales_id}"]}
#     except Exception as e:
#         return {"messages": [f"更新失败，错误原因：{e}"]}
#     finally:
#         session.close()


# # 4. 查询销售数据（暂时注释，避免数据库连接问题）
# @tool(args_schema=QuerySalesSchema)
# def query_sales(sales_id):
#     """Query sale record from the database."""
#     session = Session()
#     try:
#         sale_data = session.query(SalesData).filter(SalesData.sales_id == sales_id).first()
#         if sale_data:
#             return {
#                 "sales_id": sale_data.sales_id,
#                 "product_id": sale_data.product_id,
#                 "employee_id": sale_data.employee_id,
#                 "customer_id": sale_data.customer_id,
#                 "sale_date": sale_data.sale_date,
#                 "quantity": sale_data.quantity,
#                 "amount": sale_data.amount,
#                 "discount": sale_data.discount
#             }
#         else:
#             return {"messages": [f"未找到销售记录ID：{sales_id}。"]}
#     except Exception as e:
#         return {"messages": [f"查询失败，错误原因：{e}"]}
#     finally:
#         session.close()
