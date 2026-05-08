import os
import traceback
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from modules.rag_engine.knowledge_base import CulturalIPKnowledgeBase

class BusinessAgentWorkflow:
    def __init__(self, rag_engine=None, api_key=None):
        self.rag_engine = rag_engine
        # 默认走DeepSeek，也可通过.env切换为硅基流动或其他兼容API
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "deepseek-chat"),
            temperature=0.7,
            openai_api_key=os.getenv("DEEPSEEK_API_KEY", os.getenv("OPENAI_API_KEY", "")),
            openai_api_base=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
        )

    def run(self, query: str) -> str:
        ip_context = ""
        if self.rag_engine:
            try:
                docs = self.rag_engine.search(query, k=3)
                ip_context = "\n".join([doc.page_content for doc in docs])
            except Exception as e:
                ip_context = f"（检索失败：{e}）"

        try:
            strategy_prompt = ChatPromptTemplate.from_template(
                "你是一位在地文化IP活化专家。基于以下文化IP元素：\n{ip_context}\n\n"
                "针对问题：{query}\n"
                "请制定详细的商业策略，包括："
                "目标受众（社区/街道/村委会/文旅）、"
                "商业模式（产品/服务/授权/课程）、"
                "实施路径（分3阶段）、"
                "推荐适配的白泽造物产品线（触身历史课程包/数智展示包/工作坊/年度顾问）。"
            )
            strategy_chain = strategy_prompt | self.llm | StrOutputParser()
            strategy = strategy_chain.invoke({"ip_context": ip_context, "query": query})

            budget_prompt = ChatPromptTemplate.from_template(
                "根据以下商业策略，估算预算方案（分低配/中配/高配三档，"
                "含研发、营销、运营成本、预期ROI、实施周期）：\n{strategy}"
            )
            budget_chain = budget_prompt | self.llm | StrOutputParser()
            budget = budget_chain.invoke({"strategy": strategy})

            marketing_prompt = ChatPromptTemplate.from_template(
                "针对问题：{query}\n结合商业策略：{strategy}\n"
                "制定创新的营销方案（渠道、内容、活动、KPI）。"
            )
            marketing_chain = marketing_prompt | self.llm | StrOutputParser()
            marketing = marketing_chain.invoke({"query": query, "strategy": strategy})

            context_display = ip_context[:500] + ("..." if len(ip_context) > 500 else "")

            return (
                "\n## 白泽造物·IP活化决策报告\n\n"
                "### 检索到的在地文化IP元素\n"
                f"{context_display}\n\n"
                "### 商业策略分析\n"
                f"{strategy}\n\n"
                "### 预算估算（三档方案）\n"
                f"{budget}\n\n"
                "### 营销方案\n"
                f"{marketing}\n\n"
                "---\n"
                "*报告由白泽造物AI商业Agent自动生成*"
            )
        except Exception as e:
            error_msg = f"生成报告失败：{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return f"生成报告失败：{str(e)}"
